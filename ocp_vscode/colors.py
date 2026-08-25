"""Colour maps, re-exported.

The catalogue is `ocp_viewer_core.colors`, shared with every client - every one
of them wants the same tab10, and `_show` recognises a colormap by a base class
that has to be one class rather than one per host.

Kept as a module so that `from ocp_vscode.colors import ColorMap` still names
something. `get_colormap` was module-level here before the colormap in force
moved onto the Viewer; the re-export from show.py keeps the historic deep
import valid, and it is the same bound function as `from ocp_vscode import
get_colormap`.
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

from ocp_viewer_core.colors import BaseColorMap, ColorMap, web_to_rgb

from .show import get_colormap

__all__ = ["BaseColorMap", "ColorMap", "get_colormap", "web_to_rgb"]
