import hashlib
import os
import re
import sys

from ruamel.yaml import YAML


def add_hashes(config, root_dir="."):
    def _do(config, section):
        for key, value in config.get(section, {}).items():
            file = value.get("file")
            name = value.get("name")
            if not file or not name:
                continue

            path = os.path.join(root_dir, file)
            with open(path, "rb") as artifact:
                digest = hashlib.md5(artifact.read()).hexdigest()
            value["name"] = f"{value['name']}-{digest}"

    _do(config, "secrets")
    _do(config, "configs")


def print_help():
    print(
        "Appends docker-compose secret's and config's names with corresponding hashes of file contents",
        file=sys.stderr,
    )
    print(
        f"Usage: {sys.argv[0]} [CONFIG_ROOT_DIR] < docker-compose.template.yaml > docker-compose.yaml",
        file=sys.stderr,
    )


def main():
    root_dir = "."

    if len(sys.argv) > 2:
        print_help()
        sys.exit(1)

    if len(sys.argv) == 2:
        if sys.argv[1] in {"help", "-h", "--help"}:
            print_help()
            sys.exit(0)
        root_dir = sys.argv[1]

    yaml = YAML()
    config = yaml.load(sys.stdin)
    add_hashes(config, root_dir)
    yaml.dump(config, sys.stdout)
