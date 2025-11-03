"""
Order - Represents a confirmed purchase order
Member 3 responsibility

Complexity: Medium
"""

from decimal import Decimal
from typing import List, Any
import datetime


class Order:
    """
    Represents a customer order with items, delivery details, and status tracking.
    Created by CheckoutService; status updated through order lifecycle.
    """

    _ALLOWED_STATUSES = {"PENDING", "PAID", "FULFILLED", "SHIPPED", "DELIVERED", "CANCELLED"}

    def __init__(
        self,
        id: str,
        items: List[Any],
        address: Any,
        shipping: Decimal,
        total: Decimal,
        status: str = "PENDING",
    ) -> None:
        """
        Initialize an order.
        """
        # id
        if not isinstance(id, str) or not id.strip():
            raise ValueError("id is required")
        self._id = id.strip()

        # items
        if not isinstance(items, list) or len(items) == 0:
            raise ValueError("items must be a non-empty list")
        self._items = list(items)  # defensive copy

        # address
        if address is None:
            raise ValueError("address is required")
        self._address = address

        # money
        self._shipping = Decimal(str(shipping))
        if self._shipping < Decimal("0.00"):
            raise ValueError("shipping cannot be negative")

        self._total = Decimal(str(total))
        if self._total <= Decimal("0.00"):
            raise ValueError("total must be positive")

        # status
        if not isinstance(status, str) or status.strip() not in self._ALLOWED_STATUSES:
            raise ValueError(f"status must be one of {sorted(self._ALLOWED_STATUSES)}")
        self._status = status.strip()

        # timestamps
        self._created_at = datetime.datetime.now()
        self._paid_at: datetime.datetime | None = None

    # --- properties ---
    @property
    def id(self) -> str:
        """Read-only access to order ID."""
        return self._id

    @property
    def items(self) -> List[Any]:
        """
        Read-only access to order items.

        Returns:
            Copy of items list to prevent external modification
        """
        return list(self._items)

    @property
    def address(self) -> Any:
        """Read-only access to delivery address."""
        return self._address

    @property
    def shipping(self) -> Decimal:
        """Read-only access to shipping cost."""
        return self._shipping

    @property
    def total(self) -> Decimal:
        """Read-only access to order total."""
        return self._total

    @property
    def status(self) -> str:
        """Read-only access to order status."""
        return self._status

    @property
    def created_at(self) -> datetime.datetime:
        """Read-only access to creation timestamp."""
        return self._created_at

    @property
    def paid_at(self) -> datetime.datetime | None:
        """
        Read-only access to payment timestamp.

        Returns:
            Timestamp when order was paid, or None if not yet paid
        """
        return self._paid_at

    # --- behaviour ---
    def mark_paid(self) -> None:
        """
        Mark order as paid and record timestamp.
        Called by CheckoutService after successful payment.
        Used in Scenario 3.
        """
        if self._status != "PENDING":
            raise ValueError("Order can only be paid from PENDING status")
        self._status = "PAID"
        self._paid_at = datetime.datetime.now()

    def calculate_subtotal(self) -> Decimal:
        """
        Calculate subtotal from order items.

        Returns:
            Sum of all item subtotals
        """
        total = Decimal("0.00")
        for it in self._items:
            # Prefer a provided subtotal() method if present; otherwise unit_price * qty
            if hasattr(it, "subtotal") and callable(getattr(it, "subtotal")):
                total += Decimal(str(it.subtotal()))
            else:
                unit_price = Decimal(str(getattr(it, "unit_price")))
                qty = int(getattr(it, "qty"))
                total += unit_price * qty
        return total

    def to_dict(self) -> dict:
        """
        Convert order to dictionary format for display/storage.

        Returns:
            Dictionary with order details
        """
        # Items as dicts
        item_dicts: List[dict] = []
        for it in self._items:
            if hasattr(it, "to_dict") and callable(getattr(it, "to_dict")):
                item_dicts.append(it.to_dict())
            else:
                # Minimal fallback
                item_dicts.append(
                    {
                        "product_id": getattr(it, "product_id", None),
                        "name": getattr(it, "name", None),
                        "unit_price": getattr(it, "unit_price", None),
                        "qty": getattr(it, "qty", None),
                        "subtotal": getattr(it, "subtotal")() if hasattr(it, "subtotal") else None,
                    }
                )

        # Address as dict
        if hasattr(self._address, "to_dict") and callable(getattr(self._address, "to_dict")):
            addr_dict = self._address.to_dict()
        else:
            addr_dict = {
                "street": getattr(self._address, "street", None),
                "city": getattr(self._address, "city", None),
                "state": getattr(self._address, "state", None),
                "postcode": getattr(self._address, "postcode", None),
            }

        return {
            "id": self._id,
            "items": item_dicts,
            "address": addr_dict,
            "shipping": self._shipping,
            "total": self._total,
            "status": self._status,
            "created_at": self._created_at.isoformat(),
            "paid_at": self._paid_at.isoformat() if self._paid_at else None,
        }

    # Methods that would be implemented in full system:
    # - mark_fulfilled() -> None
    # - mark_shipped(tracking_number: str) -> None
    # - mark_delivered() -> None
    # - cancel() -> None
    # - add_tracking(tracking_number: str, carrier: str) -> None
    # - Valid status transitions would be enforced (state machine pattern)
