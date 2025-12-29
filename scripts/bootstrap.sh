#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root_dir"

python_bin="${PYTHON:-python3}"
venv_dir="${VENV_DIR:-.venv}"

if ! command -v "$python_bin" >/dev/null 2>&1; then
  echo "error: '$python_bin' not found (set PYTHON=python3.12 etc.)" >&2
  exit 1
fi

if [[ ! -d "$venv_dir" ]]; then
  "$python_bin" -m venv "$venv_dir"
fi

"$venv_dir/bin/python" -m pip install -r requirements.txt

if [[ "${1:-}" == "--xgb" ]]; then
  "$venv_dir/bin/python" -m pip install -r requirements-xgb.txt
fi

echo "ok: venv ready at $venv_dir"
