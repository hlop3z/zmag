from pathlib import Path
from string import Template


class Operations:
    def __init__(self, base_dir: Path, operations_file: Path, fragments: dict = None):
        self.base_dir = base_dir
        self.model = {}
        self.load_template(operations_file)
        if fragments:
            self.load_fragments(fragments)

    def fragment(self, model: str, fragments_file: Path):
        query = self.operations.safe_substitute({"MODEL": f"{model}"})
        with open(self.base_dir / fragments_file, "r", encoding="utf-8") as file:
            query += file.read()
        # Register
        self.model[model] = query

    def load_template(self, operations_file):
        with open(self.base_dir / operations_file, "r", encoding="utf-8") as file:
            self.operations = Template(file.read())

    def load_fragments(self, fragments):
        for key, val in fragments.items():
            self.fragment(key, val)
