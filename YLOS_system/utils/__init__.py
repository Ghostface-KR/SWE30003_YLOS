# YLOS_system/utils/__init__.py
from importlib import resources
from pathlib import Path
import json

def load_products_json() -> dict:
    """
    Load products.json from the packaged folder first (YLOS_system/data),
    then fall back to the repo-root /data for backward compatibility.
    """
    # 1) Prefer packaged resource (no cwd issues)
    try:
        txt = (resources.files("YLOS_system") / "data" / "products.json").read_text(encoding="utf-8")
        return json.loads(txt)
    except FileNotFoundError:
        pass

    # 2) Fallback to repo-root /data
    root = Path(__file__).resolve().parents[2] / "data" / "products.json"
    if root.exists():
        return json.loads(root.read_text(encoding="utf-8"))

    raise FileNotFoundError(
        "products.json not found in YLOS_system/data or in repo-root /data."
    )