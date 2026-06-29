from pathlib import Path

IGNORE = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
}

def print_tree(path: Path, prefix=""):
    entries = sorted(
        [p for p in path.iterdir() if p.name not in IGNORE],
        key=lambda x: (x.is_file(), x.name.lower())
    )

    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "

        print(prefix + connector + entry.name)

        if entry.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            print_tree(entry, prefix + extension)


root = Path.cwd()     

print(root.name)
print_tree(root)