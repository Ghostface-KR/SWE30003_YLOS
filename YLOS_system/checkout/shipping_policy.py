from decimal import Decimal
from typing import Optional
from YLOS_system.protocols import CartPort

class ShippingPolicy:
    """
    Simple shipping rules provider.
    Computes SHIPPING ONLY (not grand total).
    CheckoutService will do: total = cart.subtotal() + shipping.
    Note: The `address` parameter is accepted but not yet used in calculations.
    """

    def __init__(self, flat_rate: Decimal = Decimal("7.50"), free_over: Optional[Decimal] = None) -> None:
        # Validate and set configuration (properties removed; validation in __init__)
        if not isinstance(flat_rate, Decimal):
            raise TypeError("flat_rate must be a Decimal")
        if flat_rate < Decimal("0.00"):
            raise ValueError("flat_rate cannot be negative")
        self._flat_rate = flat_rate

        if free_over is not None:
            if not isinstance(free_over, Decimal):
                raise TypeError("free_over must be a Decimal or None")
            if free_over < Decimal("0.00"):
                raise ValueError("free_over cannot be negative")
        self._free_over = free_over

    # ----- Behavior -----
    def cost_for(self, cart: CartPort, address: object) -> Decimal:
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

        return self._flat_rate

        # Optional: extend later with address-based rules (e.g., postcode/state/region surcharges) without changing this method's public signature.