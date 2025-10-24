#!/usr/bin/env python3
"""
Restructure SWE30003_YLOS repo:
- Backup old structure into backup_old_structure_YYYYmmdd_HHMMSS/
- Create new package layout with __init__.py files
- Move known files into new locations when possible
- Generate minimal stub files if missing (PaymentService, ShippingPolicy, etc.)

Run from the repo root: python restructure_repo.py
"""

from __future__ import annotations
import os, shutil, sys, time
from pathlib import Path
from textwrap import dedent

# ---------- Config ----------
ROOT = Path(__file__).resolve().parent

OLD_TOP_LEVEL = [
    "accounts", "catalogue", "checkout", "orders", "order",
    "data", "reports", "utils", "tests", "storefront",
]

NEW_DIRS = [
    "catalogue",
    "checkout",
    "orders",
    "storefront",
    "accounts",
    "utils",
    "tests",
]

# Files to seed (created only if missing)
SEED_FILES: dict[str, str] = {
    # --- checkout side (your area) ---
    "checkout/cart.py": dedent('''\
        from dataclasses import dataclass
        from decimal import Decimal
        from typing import Dict, List

        # TODO: define CartItem value object elsewhere (checkout/cart_item.py)

        class Cart:
            def __init__(self, catalogue: object) -> None:
                self._catalogue = catalogue  # expects get_product(product_id)-> dict
                self._items: Dict[str, "CartItem"] = {}

            def items(self) -> List["CartItem"]:
                # TODO: return a copy of line items
                raise NotImplementedError

            def subtotal(self) -> Decimal:
                # TODO: sum line subtotals
                raise NotImplementedError

            def is_empty(self) -> bool:
                return len(self._items) == 0

            def add(self, product_id: str, qty: int = 1) -> None:
                # TODO: snapshot name & unit_price from catalogue; add/update qty
                raise NotImplementedError

            def update_qty(self, product_id: str, qty: int) -> None:
                # TODO: set qty (>=1) or remove if 0
                raise NotImplementedError

            def remove(self, product_id: str) -> None:
                # TODO: remove item
                raise NotImplementedError

            def clear(self) -> None:
                self._items.clear()
        '''),
    "checkout/cart_item.py": dedent('''\
        from dataclasses import dataclass
        from decimal import Decimal

        @dataclass(frozen=True)
        class CartItem:
            product_id: str
            name: str
            unit_price: Decimal
            qty: int

            def subtotal(self) -> Decimal:
                return self.unit_price * self.qty
        '''),
    "checkout/address.py": dedent('''\
        from dataclasses import dataclass

        @dataclass(frozen=True)
        class Address:
            street_number: str
            street_name: str
            city: str
            state: str
            postcode: str

            def validate(self) -> list[str]:
                errors: list[str] = []
                # TODO: require non-empty fields; simple 4-digit postcode check
                return errors

            def formatted(self) -> str:
                # TODO: return one-line formatted string
                raise NotImplementedError
        '''),
    "checkout/shipping_policy.py": dedent('''\
        from decimal import Decimal

        class ShippingPolicy:
            def cost_for(self, cart: object, address: object) -> Decimal:
                # TODO: compute shipping (flat rate for demo)
                return Decimal("0.00")
        '''),
    "checkout/payment_service.py": dedent('''\
        from decimal import Decimal
        from typing import Tuple

        class PaymentService:
            def charge(self, order_id: str, amount: Decimal) -> Tuple[bool, str]:
                # TODO: simulate payment success for demo
                return True, f"Payment of ${amount} processed. Order {order_id} confirmed"
        '''),
    "checkout/checkout_service.py": dedent('''\
        from dataclasses import dataclass
        from decimal import Decimal
        from typing import Tuple

        @dataclass
        class CheckoutService:
            cart: object
            shipping_policy: object
            payment_service: object
            order_factory: object
            account_service: object | None = None

            def compute_totals(self, address: object) -> Tuple[Decimal, Decimal, Decimal]:
                # TODO: validate cart & address; compute subtotal, shipping, total
                raise NotImplementedError

            def place_order(self, address: object, save_to_account: bool = False) -> Tuple[str, str]:
                # TODO: create pending Order from cart, charge via PaymentService;
                # on success: order.mark_paid(), cart.clear(), optionally save address
                raise NotImplementedError
        '''),
    # --- catalogue (member 1) ---
    "catalogue/catalogue.py": dedent('''\
        class Catalogue:
            def get_product(self, product_id: str) -> dict | None:
                # TODO: return {"id":..., "name":..., "price":..., "stock":...}
                return None
        '''),
    "catalogue/product.py": "class Product:\n    pass\n",
    "catalogue/product_type.py": "class ProductType:\n    pass\n",

    # --- orders (member 3) ---
    "orders/order.py": dedent('''\
        from dataclasses import dataclass, field
        from decimal import Decimal
        from typing import List

        @dataclass
        class Order:
            id: str
            items: List["OrderItem"]
            address: object
            shipping: Decimal
            total: Decimal
            status: str = "PENDING"

            def mark_paid(self) -> None:
                self.status = "PAID"
        '''),
    "orders/order_item.py": dedent('''\
        from dataclasses import dataclass
        from decimal import Decimal

        @dataclass(frozen=True)
        class OrderItem:
            product_id: str
            name: str
            unit_price: Decimal
            qty: int

            def subtotal(self) -> Decimal:
                return self.unit_price * self.qty
        '''),
    "storefront/storefront.py": "class StoreFront:\n    pass\n",
    "accounts/account.py": "class Account:\n    pass\n",
    "utils/helpers.py": "def slugify(s: str) -> str:\n    return s.strip().lower().replace(' ', '-')\n",
    "tests/test_cart.py": "def test_placeholder():\n    assert True\n",
    "tests/test_checkout_service.py": "def test_placeholder():\n    assert True\n",
    "tests/test_order.py": "def test_placeholder():\n    assert True\n",
}

# Known files to move from old places into new tree (if they exist)
MOVE_MAP = {
    # old_path -> new_path
    "checkout/checkout_service.py": "checkout/checkout_service.py",
    "main.py": "main.py",
    "README.md": "README.md",
    "requirements.txt": "requirements.txt",
}

# ---------- Helpers ----------
def confirm() -> None:
    print("This will BACK UP your existing folders and create a new structure.")
    ans = input("Proceed? [y/N]: ").strip().lower()
    if ans not in ("y", "yes"):
        print("Cancelled.")
        sys.exit(0)

def ensure_inits(dir_path: Path) -> None:
    (dir_path / "__init__.py").write_text("", encoding="utf-8")

def backup_old_tree(backup_dir: Path) -> None:
    backup_dir.mkdir(parents=True, exist_ok=True)
    for name in OLD_TOP_LEVEL:
        p = ROOT / name
        if p.exists():
            shutil.move(str(p), str(backup_dir / p.name))
    # Also back up any stray .py modules at top level except this script
    for py in ROOT.glob("*.py"):
        if py.name not in {"restructure_repo.py"}:
            shutil.move(str(py), str(backup_dir / py.name))

def create_new_tree() -> None:
    for d in NEW_DIRS:
        path = ROOT / d
        path.mkdir(parents=True, exist_ok=True)
        ensure_inits(path)

def move_known_files(backup_dir: Path) -> None:
    for old_rel, new_rel in MOVE_MAP.items():
        old = backup_dir / old_rel
        new = ROOT / new_rel
        if old.exists():
            new.parent.mkdir(parents=True, exist_ok=True)
            if not (new.parent / "__init__.py").exists():
                ensure_inits(new.parent)
            shutil.move(str(old), str(new))

def seed_files() -> None:
    for rel_path, content in SEED_FILES.items():
        dest = ROOT / rel_path
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not (dest.parent / "__init__.py").exists():
                ensure_inits(dest.parent)
            dest.write_text(content, encoding="utf-8")

def main() -> None:
    confirm()
    ts = time.strftime("%Y%m%d_%H%M%S")
    backup_dir = ROOT / f"backup_old_structure_{ts}"
    print(f"Backing up old structure to: {backup_dir}")
    backup_old_tree(backup_dir)

    print("Creating new directory tree...")
    create_new_tree()

    print("Moving known files from backup (if present)...")
    move_known_files(backup_dir)

    print("Seeding missing modules with safe stubs...")
    seed_files()

    print("\nDone.")
    print(f"- New structure created under: {ROOT}")
    print(f"- Your previous files are in:  {backup_dir}")
    print("Review moved files and stubs, then delete the backup when happy.")

if __name__ == "__main__":
    main()