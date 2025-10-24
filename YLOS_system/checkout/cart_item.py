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
