#!/usr/bin/env python3
"""Check documentation/docs/pages/experiments.yaml against experiments.schema.json.

Run from anywhere:  python documentation/scripts/validate_experiments.py [path/to/experiments.yaml]
Needs:              pip install pyyaml jsonschema
Exits non-zero, listing every problem, if the file is invalid.
"""
import json
import sys
from collections import Counter
from pathlib import Path

import jsonschema
import yaml

PAGES = Path(__file__).resolve().parent.parent / "docs" / "pages"
DATA = PAGES / "experiments.yaml"
SCHEMA = PAGES / "experiments.schema.json"


class TextDateLoader(yaml.SafeLoader):
    """SafeLoader that keeps dates (e.g. 2026-11-02) as text, so the schema's date check
    reports invalid ones (e.g. 2026-02-30) against the entry instead of YAML crashing."""


TextDateLoader.yaml_implicit_resolvers = {
    ch: [(tag, rx) for tag, rx in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for ch, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def main():
    data = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA
    try:
        experiments = yaml.load(data.read_text(), Loader=TextDateLoader)
    except yaml.YAMLError as e:
        print(f"{data.name}: not valid YAML\n{e}")
        return 1

    schema = json.loads(SCHEMA.read_text())
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())

    problems = []
    for err in sorted(validator.iter_errors(experiments), key=lambda e: list(e.absolute_path)):
        path = list(err.absolute_path)
        where = "file"
        if path and isinstance(path[0], int):
            entry = experiments[path[0]]
            name = entry.get("experiment") if isinstance(entry, dict) else None
            where = f"entry {path[0] + 1} ({name or 'no experiment name'})"
            path = path[1:]
        field = ".".join(str(p) for p in path)
        problems.append(f"{where}: {field + ': ' if field else ''}{err.message}")

    if isinstance(experiments, list):
        names = Counter(e.get("experiment") for e in experiments if isinstance(e, dict))
        problems += [f"experiment '{n}' appears {c} times; names must be unique" for n, c in names.items() if n and c > 1]

    if problems:
        print(f"{data.name}: {len(problems)} problem(s)")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"{data.name}: {len(experiments)} experiments OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
