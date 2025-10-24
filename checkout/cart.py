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
