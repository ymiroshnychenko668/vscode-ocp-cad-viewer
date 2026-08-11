"""`python -m ocp_vscode --backend`: the measurement backend for a VS Code viewer.

This used to be two programs sharing an entry point - the standalone viewer,
and the backend the extension launches for it. The standalone is `ocp_viewer`
now, and what is left is the one the extension calls: `controller.ts` spawns
this with the port of the viewer it just opened.

The backend itself is `ocp_viewer_core.backend`, shared with every host. What
this supplies is the transport, which is the only part that is ours.
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

import argparse

from ocp_viewer_core.backend import ViewerBackend

from ocp_vscode.comms import comms, set_port


MOVED = """
Standalone OCP viewer is now part of the package ocp_viewer

    Install it via `[uv] pip install ocp_viewer`
    Run it via     `python -m ocp_viewer`
"""


def main():
    parser = argparse.ArgumentParser("OCP CAD Viewer measurement backend")
    parser.add_argument(
        "--backend",
        action="store_true",
        help="Run the measurement backend, which is what this module is for",
    )
    parser.add_argument("--port", type=int, help="Port the viewer listens on")
    args = parser.parse_args()

    # `python -m ocp_vscode` with no arguments started the standalone viewer for
    # years, so that is the command people will type. Say where it went rather
    # than answering with an argparse usage line.
    if not args.backend:
        print(MOVED)
        return

    if args.port is None:
        parser.error("--backend needs --port")

    # The backend takes a transport rather than a port: which viewer it answers,
    # and how, is this host's to say.
    set_port(args.port)
    backend = ViewerBackend(comms)

    try:
        backend.start()
    except ConnectionRefusedError:
        print(
            f"Cannot connect to OCP CAD Viewer on port {args.port}.\n"
            "This is the measurement backend, and it connects to a viewer that "
            "is already running.\nFor the standalone viewer, use `python -m "
            "ocp_viewer`."
        )
    except Exception as ex:  # noqa: BLE001
        print(ex)


if __name__ == "__main__":
    main()
