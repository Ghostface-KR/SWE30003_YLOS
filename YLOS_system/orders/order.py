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
