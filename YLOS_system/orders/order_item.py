"""
OrderItem - Represents a single line item in an order
Member 3 responsibility
Complexity: Simple (Data Holder)
"""

from decimal import Decimal


class OrderItem:
    """
    Immutable snapshot of a product at the time of order placement.
    Similar to CartItem but represents a confirmed purchase.
    """

    def __init__(self, product_id: str, name: str, unit_price: Decimal, qty: int) -> None:
        """
        Initialize an order item.
        """
        # --- Validation ---
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("product_id must be a non-empty string")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")

        # Ensure unit_price is Decimal
        try:
            price = Decimal(str(unit_price))
        except Exception:
            raise TypeError("unit_price must be convertible to Decimal")

        if price < Decimal("0.00"):
            raise ValueError("unit_price cannot be negative")

        if not isinstance(qty, int) or isinstance(qty, bool):
            raise TypeError("qty must be an integer")
        if qty < 1:
            raise ValueError("qty must be at least 1")

        # --- Store as private attributes ---
        self._product_id = product_id.strip()
        self._name = name.strip()
        self._unit_price = price
        self._qty = qty

    @property
    def product_id(self) -> str:
        """Read-only access to product ID."""
        return self._product_id

    @property
    def name(self) -> str:
        """Read-only access to product name."""
        return self._name

    @property
    def unit_price(self) -> Decimal:
        """Read-only access to unit price."""
        return self._unit_price

    @property
    def qty(self) -> int:
        """Read-only access to quantity."""
        return self._qty

    def subtotal(self) -> Decimal:
        """
        Calculate line item total.
        Returns: unit_price * qty
        """
        return self._unit_price * self._qty

    def to_dict(self) -> dict:
        """
        Convert to dictionary format.
        Returns a dictionary with all item details.
        """
        return {
            "product_id": self._product_id,
            "name": self._name,
            "unit_price": self._unit_price,
            "qty": self._qty,
            "subtotal": self.subtotal(),
        }

    # Methods that would be implemented in full system:
    # - with_qty(new_qty: int) -> OrderItem  # Not needed for orders (immutable after creation)
    # - equals(other: OrderItem) -> bool  # For comparison
