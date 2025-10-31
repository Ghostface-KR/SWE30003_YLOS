from decimal import Decimal

class CartItem:
    """
    Immutable-like snapshot of a cart line at add-time.
    Exposes read-only properties; use with_qty(...) to 'change' quantity (returns a NEW instance).
    """

    def __init__(self, product_id: str, name: str, unit_price: Decimal, qty: int) -> None:
        # "private-ish" storage using single leading underscores for consistency

        self._product_id = product_id          # read-only (public via property)
        self._name = name                      # read-only (public via property)
        # normalize then validate, then store
        unit_price = Decimal(str(unit_price))  # convert once to Decimal (avoids float artifacts)
        if unit_price < 0:
            raise ValueError("unit_price must be >= 0")
        self._unit_price = unit_price
        if qty < 1:
            raise ValueError("qty must be >= 1")  # Ensure quantity is at least 1
        self._qty = qty                        # guarded by property


    # ----- Read-only public properties -----
    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def unit_price(self) -> Decimal:
        """Unit price captured at add-time (read-only)."""
        return self._unit_price

    @property
    def qty(self) -> int:
        """Quantity for this line (read-only)."""
        return self._qty

    # ----- Behavior -----
    def subtotal(self) -> Decimal:
        """
        Line total at the captured price.
        """
        # Calculate and return the subtotal for cart item.
        subtotal = (self.unit_price * self._qty)
        return subtotal


    def with_qty(self, new_qty: int) -> "CartItem":
        """
        Return a NEW CartItem with updated quantity (immutability).
        """
        # Delegate validation to the constructor to keep rules in one place.
        return CartItem(self.product_id, self.name, self.unit_price, new_qty)
