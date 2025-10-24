from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Optional

# NOTE: Expect a CartItem value object elsewhere in your codebase:
# @dataclass(frozen=True)
# class CartItem:
#     product_id: str
#     name: str
#     unit_price: Decimal
#     qty: int
#     def subtotal(self) -> Decimal: return self.unit_price * qty

class Cart:
    """
    Holds CartItem snapshots (id, name, unit_price, qty).
    Fetches current product info from a Catalogue ONLY when adding items.
    After that, prices come from the CartItems (snapshots).
    """

    def __init__(self, catalogue: object) -> None:
        self._catalogue = catalogue  # TODO: provide get_product(product_id)-> {name, price, stock}
        self._items: Dict[str, "CartItem"] = {}

    # ----- Queries -----
    def items(self) -> List["CartItem"]:
        """Return a list of current CartItems (read-only)."""
        # TODO: return a copy to avoid external mutation
        return list(self._items.values())

    def subtotal(self) -> Decimal:
        """Sum of line subtotals (no shipping or tax)."""
        # TODO: sum(item.subtotal() for item in self._items.values())
        raise NotImplementedError

    def is_empty(self) -> bool:
        """True if the cart has no items."""
        return len(self._items) == 0

    # ----- Commands -----
    def add(self, product_id: str, qty: int = 1) -> None:
        """
        Add a product (creates/updates a CartItem snapshot with current name & price).
        """
        # TODO: guard: qty >= 1
        # TODO: fetch = self._catalogue.get_product(product_id)
        #       validate product exists
        #       validate stock >= (existing_qty + qty)
        # TODO: snapshot name and unit_price = Decimal(str(fetch["price"]))
        # TODO: if exists: new_qty = old.qty + qty (validate >=1)
        #       update CartItem with new_qty (immutably)
        # TODO: else: create CartItem(product_id, name, unit_price, qty)
        raise NotImplementedError

    def update_qty(self, product_id: str, qty: int) -> None:
        """
        Set a new quantity for an item; remove if qty == 0.
        """
        # TODO: if product not in cart -> no-op or raise
        # TODO: if qty == 0: remove and return
        # TODO: guard: qty >= 1
        # TODO: check stock in catalogue >= qty
        # TODO: rebuild CartItem with same snapshot name/unit_price, new qty
        raise NotImplementedError

    def remove(self, product_id: str) -> None:
        """Remove an item entirely."""
        # TODO: pop from dict if present
        raise NotImplementedError

    def clear(self) -> None:
        """Empty the cart after a successful order."""
        self._items.clear()

    # ----- Convenience for demo/UI (optional) -----
    def view_summary(self) -> dict:
        """
        Lightweight read-model for CLI/UI (lines + subtotal).
        """
        # TODO: return {
        #   "lines": [{"id": i.product_id, "name": i.name, "qty": i.qty, "unit_price": str(i.unit_price),
        #              "subtotal": str(i.subtotal())} for i in self.items()],
        #   "subtotal": str(self.subtotal())
        # }
        raise NotImplementedError