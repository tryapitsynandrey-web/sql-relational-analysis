"""
Notebook structure validator for the Olist analytics pipeline.

Verifies that every ``.ipynb`` file in ``analysis/notebooks/`` contains
the three mandatory executive conclusion sections and that all code cells
are syntactically valid Python. Exits with code 1 if any notebook fails.

Run from the repository root:
    python scripts/validate_notebooks.py
"""
from pathlib import Path
import json
import ast
import sys

REQUIRED_SECTIONS = [
    "Key Findings",
    "Business Implications",
    "Actionable Recommendations",
]

def validate_notebook(nb_path: Path) -> list[str]:
    with nb_path.open(encoding="utf-8") as f:
        nb = json.load(f)

    code_blocks = []
    text_blocks = []
    
    for cell in nb.get("cells", []):
        src = "".join(cell.get("source", []))
        text_blocks.append(src)
        if cell.get("cell_type") == "code":
            code_blocks.append(src)

    code = "\n".join(code_blocks)
    full_text = "\n".join(text_blocks)

    # syntax check
    ast.parse(code)

    missing = [s for s in REQUIRED_SECTIONS if s not in full_text]
    return missing

def main():
    errors = {}

    for nb in Path("analysis/notebooks").glob("*.ipynb"):
        try:
            missing = validate_notebook(nb)
            if missing:
                errors[nb.name] = f"Missing sections: {missing}"
        except Exception as e:
            errors[nb.name] = str(e)

    if errors:
        print("FAILED:")
        for k, v in errors.items():
            print(f"- {k}: {v}")
        sys.exit(1)

    print("All notebooks valid.")

if __name__ == "__main__":
    main()