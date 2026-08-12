"""Configuration of the viewer.

The semantics live in `ocp_viewer_core.config`. What is ocp_vscode's, and stays
here, is the two lists that tell the core what this host can do, the transport
it is built on, and the names bound off the instance so that
`from ocp_vscode import show, status, set_defaults` keeps working.

The `JUPYTER_CADQUERY` import branch this module opened with is gone. It decided
at import time, from an environment variable, which transport the config
functions would use - so `from ocp_vscode import config` behaved differently
depending on a variable set somewhere else. A host supplying its own `Comms` is
that decision made in one place, by the host, at construction.
"""

#
# Copyright 2025 Bernhard Walter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from ocp_viewer_core.comms import Session
from ocp_viewer_core.config import (
    AnalysisTool,
    Camera,
    Collapse,
    Config,
    Render,
    StudioBackground,
    StudioEnvironment,
    StudioTextureMapping,
    StudioToneMapping,
    UiTab,
)

from ocp_vscode.comms import comms

__all__ = [
    "workspace_config",
    "combined_config",
    "set_viewer_config",
    "set_defaults",
    "reset_defaults",
    "get_default",
    "get_defaults",
    "status",
    "AnalysisTool",
    "Camera",
    "Collapse",
    "Render",
    "StudioEnvironment",
    "StudioBackground",
    "StudioToneMapping",
    "StudioTextureMapping",
    "UiTab",
    "check_deprecated",
]

# The keys of the viewer's own state that survive into a show's config.
#
# `Config.workspace_filter` uses this list to decide which of the viewer's
# reported state survives into the next show, so it has to name every key the
# user can change from the toolbar - the toggles, clip, zebra and studio, the
# active tab, explode and the analysis tool. A shorter list, such as one naming
# only the keys this client stores in its settings, would let a second show()
# reset the user's toolbar to the workspace defaults.

WORKSPACE_CONFIG_KEYS = (
    "ambient_intensity",
    "analysis_tool",
    "angular_tolerance",
    "axes",
    "axes0",
    "black_edges",
    "center_grid",
    "clip_intersection",
    "clip_normal_0",
    "clip_normal_1",
    "clip_normal_2",
    "clip_object_colors",
    "clip_planes",
    "clip_slider_0",
    "clip_slider_1",
    "clip_slider_2",
    "collapse",
    "default_color",
    "default_edgecolor",
    "default_facecolor",
    "default_opacity",
    "default_thickedgecolor",
    "default_vertexcolor",
    "deviation",
    "direct_intensity",
    "explode",
    "glass",
    "grid",
    "grid_font_size",
    "metalness",
    "modifier_keys",
    "orbit_control",
    "ortho",
    "pan_speed",
    "rotate_speed",
    "roughness",
    "states",
    "studio_4k_env_maps",
    "studio_ao_intensity",
    "studio_background",
    "studio_env_intensity",
    "studio_env_rotation",
    "studio_environment",
    "studio_exposure",
    "studio_shadow_intensity",
    "studio_shadow_softness",
    "studio_texture_mapping",
    "studio_tone_mapping",
    "tab",
    "theme",
    "ticks",
    "tools",
    "transparent",
    "tree_width",
    "up",
    "zebra_color_scheme",
    "zebra_count",
    "zebra_direction",
    "zebra_mapping_mode",
    "zebra_opacity",
    "zoom_speed",
)

# The keywords that belong to other hosts. The show signature is the superset of
# every client's, so a key one host owns is a key another has to refuse - and
# refusing it by name is what tells a user their `anchor=` went nowhere instead
# of leaving them to wonder.
#
# `cad_width` and `height` are this surface's own to decide, where a notebook
# cell is told them; `viewer`, `anchor` and `pinning` name a sidecar this host
# does not have.
EXCLUDE_KEYS = ("cad_width", "height", "viewer", "anchor", "pinning")

# The client from comms.py, not a second one: `set_port()` points that
# instance at a viewer, and a Session built on a different one would not hear
# about it.
session = Session(comms)
config = Config(session, WORKSPACE_CONFIG_KEYS, EXCLUDE_KEYS)

# Bound methods, not wrappers: the signature is the documentation for these two,
# and a wrapper would have to restate fifty keywords to keep completion on them.

set_defaults = config.set_defaults
set_viewer_config = config.set_viewer_config
check_deprecated = config.check_deprecated
validate_tool_args = config.validate_tool_args


# The small entry points keep the host keyword they have always taken, and open
# the scope so the transport can act on it. Only `port`: `viewer` names Jupyter
# CadQuery's sidecar and was accepted here and passed to a transport that
# ignores it. The superset belongs to the show family, which is one signature
# serving four hosts; these functions are this host's own.
#
# These wrap rather than nest: the core's own calls between these methods
# (`combined_config` asks itself for `status` and `workspace_config`) go
# straight to the methods, never back through here, so no scope is opened twice.


def status(port=None, debug=False):
    """Get viewer status"""
    session.begin({"port": port})
    try:
        return config.status(debug=debug)
    finally:
        session.clear()


def workspace_config(port=None):
    """Get viewer workspace config"""
    session.begin({"port": port})
    try:
        return config.workspace_config()
    finally:
        session.clear()


def combined_config(port=None):
    """Get combined config from workspace and status"""
    session.begin({"port": port})
    try:
        return config.combined_config()
    finally:
        session.clear()


def get_changed_config(key=None, port=None):
    """Get changed config from workspace and status"""
    session.begin({"port": port})
    try:
        return config.get_changed_config(key=key)
    finally:
        session.clear()


def get_defaults(port=None):
    """Get all defaults"""
    session.begin({"port": port})
    try:
        return config.get_defaults()
    finally:
        session.clear()


def get_default(key, port=None):
    """Get default value for key"""
    session.begin({"port": port})
    try:
        return config.get_default(key)
    finally:
        session.clear()


def preset(key, value, port=None):
    """The default for key, unless a value was given"""
    session.begin({"port": port})
    try:
        return config.preset(key, value)
    finally:
        session.clear()


def reset_defaults(port=None):
    """Reset defaults not given in workspace config"""
    session.begin({"port": port})
    try:
        return config.reset_defaults()
    finally:
        session.clear()
