"""The show family, bound to this host's viewer.

The pipeline itself - `_tessellate`, `_convert`, `_show`, and the whole show
family around them - is `ocp_viewer_core.show.Viewer`. What is left here is the
one `Viewer` this process shows through, and the names bound off it.

They are bound methods and nothing else, deliberately. `show` carries 84
keywords and `show_object` 85; a wrapper would have to restate every one of them
to keep hover and completion, and `functools.partial` and `functools.wraps` both
lose them - partial hovers with no parameters at all, wraps leaks the config
object into the visible ones. Measured with basedpyright before the shape was
chosen. A bound method hovers with the full signature, `self` gone.

`show_all` has a second reason: it reads its caller's frame through
`inspect.currentframe().f_back` to find the variables to draw. Wrapped, that
frame would be the wrapper's.

Which transport a show uses is the `Comms` this host built its `Config` on,
decided once at construction rather than by an environment variable read at
import time.
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

from ocp_viewer_core.show import Viewer, ignore_camera_warnings, none_filter

from ocp_vscode.config import config

__all__ = [
    "Animation",
    "show",
    "show_object",
    "remove_object",
    "_show",
    "_show_object",
    "push_object",
    "show_objects",
    "reset_show",
    "show_all",
    "show_clear",
    "save_screenshot",
    "none_filter",
    "ignore_camera_warnings",
    "get_colormap",
    "set_colormap",
    "unset_colormap",
]

# `None` is the handle type: the webview hands nothing back, so `show` returns
# None here. A host whose transport returns a widget binds its widget class
# instead and its users get that type from the same definition.
viewer = Viewer[None](config)

show = viewer.show
show_object = viewer.show_object
show_objects = viewer.show_objects
show_all = viewer.show_all
show_clear = viewer.show_clear
push_object = viewer.push_object
remove_object = viewer.remove_object
reset_show = viewer.reset_show
save_screenshot = viewer.save_screenshot

_show = viewer._show
_show_object = viewer._show_object

# The colormap in force belongs to the Viewer, along with the object stack and
# the last bounding box, so that two viewers in one process keep their own.
get_colormap = viewer.get_colormap
set_colormap = viewer.set_colormap
unset_colormap = viewer.unset_colormap

# The animation module resolves the paths a user names against the last
# tessellated tree, which is the Viewer's now rather than a module global.
get_last_paths = viewer.get_last_paths

# The core's Animation, bound like the show family: `Animation()` constructs
# an animation over this viewer's last show.
Animation = viewer.animation
