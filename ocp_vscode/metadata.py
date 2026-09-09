"""Carry source metadata through tessellation without matching display names.

The tessellator deliberately handles geometry and appearance only. These small
converter hooks retain the association with the original Python object until
the tessellator has assigned the final viewer paths (including duplicate names).
No global monkeypatch or STEP-library dependency is needed by the viewer.
"""

import json

from ocp_tessellate.convert import OcpConverter
from ocp_tessellate.cad_objects import OcpGroup


def _metadata(cad_obj, rendered):
    source = getattr(cad_obj, "cad_metadata", None)
    if source is not None:
        if not isinstance(source, dict):
            raise TypeError("Shape.cad_metadata must be a JSON object")
        # Validate, detach mutable model state, and reject non-JSON OCCT handles.
        data = json.loads(json.dumps(source, ensure_ascii=False, allow_nan=False))
    else:
        data = {}
    current = data.setdefault("current", {})
    current["name"] = rendered.name
    color = getattr(rendered, "color", None)
    if color is not None:
        current["display_color"] = list(color.percentage)
    data.setdefault("schema_version", 1)
    data.setdefault("kind", "assembly" if isinstance(rendered, OcpGroup) else "body")
    return data


class MetadataConverter(OcpConverter):
    """Retain metadata on the exact converted assembly/shape object."""

    def handle_build123d_assembly(self, cad_obj, *args, **kwargs):
        result = super().handle_build123d_assembly(cad_obj, *args, **kwargs)
        result.cad_metadata = _metadata(cad_obj, result)
        return result

    def handle_shapes(self, cad_obj, *args, **kwargs):
        result = super().handle_shapes(cad_obj, *args, **kwargs)
        result.cad_metadata = _metadata(cad_obj, result)
        return result


def to_ocpgroup(*cad_objs, **kwargs):
    """Equivalent to the pinned tessellator entry point, with metadata hooks."""
    options = dict(kwargs)
    converter = MetadataConverter(**{
        key: options.pop(key)
        for key in (
            "progress", "helper_scale", "render_joints", "render_mates",
            "show_parent", "show_locals", "debug",
        )
        if key in options
    })
    group = converter.to_ocp(*cad_objs, **options)
    if group.name is None:
        group.name = "Group"
    return group, converter.instances


def attach_metadata(group, shapes):
    """Add metadata to final mesh nodes using paths assigned by collect()."""
    by_id = {}

    def collect(node):
        metadata = getattr(node, "cad_metadata", None)
        if metadata is not None:
            by_id[node.id] = metadata
        if isinstance(node, OcpGroup):
            for child in node.objects:
                collect(child)

    def apply(node):
        if node["id"] in by_id:
            node["metadata"] = by_id[node["id"]]
            # make_unique_names may have changed the name after conversion.
            node["metadata"]["current"]["name"] = node["name"]
        for child in node.get("parts", []):
            apply(child)

    collect(group)
    apply(shapes)
