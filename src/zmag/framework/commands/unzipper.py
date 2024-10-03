"""
Unzip Folders
"""

import os
import pathlib
import shutil
import zipfile
from typing import Any

CURRENT_PATH = pathlib.Path(__file__).parents[0]
TEMPORARY_DIR = CURRENT_PATH / "tmp"
TEMPLATES_DIR = CURRENT_PATH.parent / "apps_templates"


def path_delete(dir_path):
    """Delete Path"""
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print(f"Error: {dir_path} : {e.strerror}")


def unzip_base(source, destination):
    """Unzip Base"""
    with zipfile.ZipFile(source, "r") as zip_ref:
        zip_ref.extractall(destination)


def unzip(source: str, destination: str) -> Any:
    """Unzip Method"""
    source_path = TEMPLATES_DIR / source
    file_name = source_path.name
    file_name = file_name.replace(".zip", "")
    unzip_base(source_path, TEMPORARY_DIR)
    shutil.move(TEMPORARY_DIR / file_name, destination)


def zipper(zip_path, source_path):
    """Zip Method"""

    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, _, files in os.walk(path):
            for file in files:
                ziph.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), os.path.join(path, "..")),
                )

    with zipfile.ZipFile(f"{str(zip_path)}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        zipdir(source_path, zipf)
