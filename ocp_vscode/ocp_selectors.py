"""Selector helpers, re-exported from the core.

The implementation moved to `ocp_viewer_core.selectors`, shared by every
viewer; this module keeps the historic deep import
`from ocp_vscode.ocp_selectors import select_faces` valid.
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

from ocp_viewer_core.selectors import (
    select_edge,
    select_edges,
    select_face,
    select_faces,
    select_vertex,
    select_vertices,
)

__all__ = [
    "select_vertex",
    "select_vertices",
    "select_edge",
    "select_edges",
    "select_face",
    "select_faces",
]
