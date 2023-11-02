"""
    Start A New Project
"""
try:
    import os
    import pathlib
    import shutil
    import zipfile

    import argparse

    TEMPLATES_DIR = pathlib.Path(__file__).parents[0]
    TEMPORARY_DIR = pathlib.Path(__file__).parents[0] / "tmp"

    def unzip_base(source, destination):
        """Unzip Base"""
        with zipfile.ZipFile(source, "r") as zip_ref:
            zip_ref.extractall(destination)

    def unzip(source: pathlib.Path, destination: pathlib.Path):
        """Unzip Method"""
        zipfile_name = source.name.replace(".zip", "")
        unzip_base(source, TEMPORARY_DIR)
        tmp = TEMPORARY_DIR / zipfile_name
        file_names = os.listdir(tmp)
        for file_name in file_names:
            try:
                shutil.move(os.path.join(tmp, file_name), destination)
            except:
                pass
        shutil.rmtree(tmp, ignore_errors=False, onerror=None)

    def start_project():
        parser = argparse.ArgumentParser(description="Start A New Project")
        parser.add_argument(
            "number", type=int, help="The number to calculate the square of"
        )
        args = parser.parse_args()
        result = args.number**2
        print(f"The square of {args.number} is {result}")

except:
    pass  # Ignore the exception
