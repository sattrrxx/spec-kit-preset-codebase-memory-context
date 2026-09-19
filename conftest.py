import os
import sys
import sysconfig
from pathlib import Path


def _prepend_path_dir(directory: str) -> None:
    path_entries = [entry for entry in os.environ.get("PATH", "").split(os.pathsep) if entry]
    if directory not in path_entries:
        os.environ["PATH"] = os.pathsep.join([directory, *path_entries])


scripts_dir = Path(sysconfig.get_path("scripts")).resolve()
if scripts_dir.exists():
    _prepend_path_dir(str(scripts_dir))

python_scripts_dir = Path(sys.executable).resolve().parent
if python_scripts_dir.exists():
    _prepend_path_dir(str(python_scripts_dir))
