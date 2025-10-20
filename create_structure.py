from pathlib import Path

base = Path("SWE30003_YLOS")

folders = [
    base / "accounts",
    base / "catalogue",
    base / "checkout",
    base / "reports",
    base / "utils",
    base / "data",
    Path("tests")
]

files = [
    "main.py",
    "requirements.txt",
    "README.md",
    ".gitignore"
]

# create folders + __init__.py
for folder in folders:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "__init__.py").touch(exist_ok=True)

# create top-level files
for f in files:
    Path(f).touch(exist_ok=True)

print("✅ SWE30003_YLOS folder structure created successfully.")
