from decimal import Decimal
from typing import Protocol

# TODO: Move CartProtocol to a shared protocols.py to avoid circular dependencies
class CartProtocol(Protocol):
    def subtotal(self) -> Decimal:
        ...

class ShippingPolicy:
    """
    Simple shipping rules provider.
    Computes SHIPPING ONLY (not grand total).
    CheckoutService will do: total = cart.subtotal() + shipping.
    Note: The `address` parameter is accepted but not yet used in calculations.
    """

    def __init__(self, flat_rate: Decimal = Decimal("7.50"), free_over: Decimal | None = None) -> None:
        # Use setters to apply validation on initialization
        self.flat_rate = flat_rate
        self.free_over = free_over

    # ----- Properties with simple guards (get/set if you extend) -----
    @property
    def flat_rate(self) -> Decimal:
        return self._flat_rate

    @flat_rate.setter
    def flat_rate(self, value: Decimal) -> None:
        # Validate that flat_rate is a non-negative Decimal; raise a clear error if invalid.
        if not isinstance(value, Decimal):
            raise TypeError("flat_rate must be a Decimal")
        if value < Decimal("0.00"):
            raise ValueError("flat_rate cannot be negative")
        self._flat_rate = value

    @property
    def free_over(self) -> Decimal | None:
        return self._free_over

    @free_over.setter
    def free_over(self, value: Decimal | None) -> None:
        # Validate that free_over is either None (disabled) or a non-negative Decimal; raise a clear error if invalid.
        if value is not None:
            if not isinstance(value, Decimal):
                raise TypeError("free_over must be a Decimal or None")
            if value < Decimal("0.00"):
                raise ValueError("free_over cannot be negative")
        self._free_over = value

    # ----- Behavior -----
    def cost_for(self, cart: CartProtocol, address: object) -> Decimal:
        """
        Return the shipping cost for the given cart + address.
        """
        # Future: use address for region-based rates (kept for compatibility)
        # Retrieve the cart's subtotal via its public API (do not mutate the cart); ensure the value is a Decimal.
        cart_subtotal = cart.subtotal()
        if not isinstance(cart_subtotal, Decimal):
            raise TypeError("cart subtotal must be a Decimal")

        # Check if free-shipping threshold applies and return zero shipping if subtotal qualifies.
        if self._free_over is not None and cart_subtotal >= self._free_over:
            return Decimal("0.00")

        return self.flat_rate

        # Optional: extend later with address-based rules (e.g., postcode/state/region surcharges) without changing this method's public signature.