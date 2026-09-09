#!/usr/bin/env bash
# Run a CAD project's preview with this Python clone and the sibling renderer.
set -euo pipefail

viewer_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
workspace_dir="$(cd -- "$viewer_dir/.." && pwd)"
python_bin="${CAD_VIEWER_PYTHON:-$workspace_dir/.venv/bin/python}"
frontend_dir="${CAD_VIEWER_FRONTEND:-$workspace_dir/three-cad-viewer}"

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 PROJECT_DIRECTORY [preview.py arguments]" >&2
    exit 2
fi
project_dir="$(cd -- "$1" && pwd)"
shift
if [[ ! -x "$python_bin" || ! -f "$project_dir/preview.py" ]]; then
    echo "Expected an executable Python at $python_bin and preview.py in $project_dir" >&2
    exit 1
fi

# Absolute path is essential: preview.py changes the server child's working dir.
export PYTHONPATH="$viewer_dir${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONUNBUFFERED=1

export_only=false
for argument in "$@"; do
    if [[ "$argument" == "--export" ]]; then export_only=true; fi
done

"$python_bin" - "$viewer_dir" "$frontend_dir" "$export_only" <<'PY'
from pathlib import Path
import json
import os
import shutil
import sys

viewer_dir = Path(sys.argv[1]).resolve()
frontend_dir = Path(sys.argv[2]).resolve()
import ocp_vscode

module_path = Path(ocp_vscode.__file__).resolve()
if not module_path.is_relative_to(viewer_dir):
    raise SystemExit(f"Wrong ocp_vscode import: {module_path}")
print(f"Python viewer source: {module_path}", flush=True)
if sys.argv[3] == "true":
    raise SystemExit(0)

assets = {
    "dist/three-cad-viewer.esm.js": "ocp_vscode/static/js/three-cad-viewer.esm.js",
    "dist/three-cad-viewer.css": "ocp_vscode/static/css/three-cad-viewer.css",
}
for source in assets:
    if not (frontend_dir / source).is_file():
        raise SystemExit(
            f"Missing renderer build: {frontend_dir / source}\n"
            f"Build first: cd '{frontend_dir}' && yarn install --frozen-lockfile"
        )

# Serve the actual dist outputs: rebuilding the renderer only needs a browser reload.
for source, destination in assets.items():
    source = frontend_dir / source
    destination = viewer_dir / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink() and destination.resolve() == source.resolve():
        continue
    if destination.exists() or destination.is_symlink():
        destination.unlink()
    destination.symlink_to(os.path.relpath(source, destination.parent))

for source, destination in (
    ("resources/viewer.html", "ocp_vscode/templates/viewer.html"),
    ("src/logo.ts", "ocp_vscode/static/js/logo.js"),
    ("resources/ocp-eye.png", "ocp_vscode/static/icon/ocp-eye.png"),
):
    source, destination = viewer_dir / source, viewer_dir / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists() or destination.read_bytes() != source.read_bytes():
        shutil.copyfile(source, destination)

version = json.loads((frontend_dir / "package.json").read_text())["version"]
print(f"Renderer source: {frontend_dir} (three-cad-viewer {version})", flush=True)
PY

exec "$python_bin" "$project_dir/preview.py" "$@"
