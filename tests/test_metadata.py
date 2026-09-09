"""Metadata must follow occurrences, not display names or shared geometry."""

from copy import deepcopy

import pytest
from build123d import Box, Color, Compound, Pos

from ocp_vscode.metadata import attach_metadata, to_ocpgroup


def mesh_nodes(*objects, **kwargs):
    group, instances = to_ocpgroup(*objects, **kwargs)
    _, shapes = group.collect("", instances)
    attach_metadata(group, shapes)
    return shapes


def test_repeated_names_and_geometry_keep_separate_metadata():
    first = Box(1, 2, 3)
    first.label = "same"
    first.cad_metadata = {"id": "occurrence-a", "properties": {"value": 0}}
    second = first.moved(Pos(10, 0, 0))
    second.cad_metadata = {"id": "occurrence-b", "properties": {"value": False}}
    assembly = Compound(label="Сборка", children=[first, second])
    assembly.cad_metadata = {"id": "assembly", "original": {"name": "原始 / name"}}
    shapes = mesh_nodes(assembly)
    assert shapes["metadata"]["id"] == "assembly"
    a, b = shapes["parts"]
    assert a["id"] != b["id"]
    assert a["metadata"]["id"] == "occurrence-a"
    assert b["metadata"]["id"] == "occurrence-b"
    assert b["metadata"]["properties"]["value"] is False
    assert a["metadata"]["current"]["name"] == a["name"]
    assert b["metadata"]["current"]["name"] == b["name"]


def test_metadata_is_detached_and_source_color_not_overwritten():
    shape = Box(1, 2, 3)
    shape.color = Color("red")
    shape.cad_metadata = {"original": {"color": "blue"}, "properties": {"nested": [1, 2]}}
    original = deepcopy(shape.cad_metadata)
    node = mesh_nodes(shape)["parts"][0]
    assert node["metadata"]["original"]["color"] == "blue"
    assert node["metadata"]["current"]["display_color"][:3] == [1.0, 0.0, 0.0]
    node["metadata"]["properties"]["nested"].append(3)
    assert shape.cad_metadata == original


def test_old_models_work_without_source_metadata():
    node = mesh_nodes(Box(1, 1, 1))["parts"][0]
    assert node["metadata"]["current"]["name"]
    assert "id" not in node["metadata"]  # No invented persistent identity.
    assert "source" not in node["metadata"]


def test_invalid_metadata_fails_before_transport():
    shape = Box(1, 1, 1)
    shape.cad_metadata = {"document": object()}
    with pytest.raises(TypeError):
        mesh_nodes(shape)
