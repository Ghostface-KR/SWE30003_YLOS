from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple, Optional

# NOTE: Collaborators expected at runtime:
# - cart: Cart (above)
# - shipping_policy: object with cost_for(cart, address) -> Decimal
# - payment_service: object with charge(order_id: str, amount: Decimal) -> (success: bool, message: str)
# - order_factory: object with create_from_cart(cart, address, shipping: Decimal) -> "Order"
#   And Order should have: id: str, total: Decimal, mark_paid().

@dataclass
class CheckoutService:
    """
    Coordinates checkout steps (validate address, compute shipping/total,
    create order, request payment, finalize on success).
    """
    cart: object
    shipping_policy: object
    payment_service: object
    order_factory: object
    account_service: Optional[object] = None  # optional: for "save this address"

    # ----- Helper queries -----
    def compute_totals(self, address: "Address") -> Tuple[Decimal, Decimal, Decimal]:
        """
        Returns (subtotal, shipping, total).
        """
        # TODO: ensure cart not empty -> if empty, raise or return sentinel
        # TODO: addr_errors = address.validate(); if any -> raise or return sentinel
        # TODO: subtotal = self.cart.subtotal()
        # TODO: shipping = self.shipping_policy.cost_for(self.cart, address)
        # TODO: total = subtotal + shipping
        raise NotImplementedError

    # ----- Main flow -----
    def place_order(
        self,
        address: "Address",
        save_to_account: bool = False
    ) -> Tuple[str, str]:
        """
        Validate address; compute shipping/total; create order (pending);
        take payment; on success mark paid + clear cart; return (order_id, message).
        """
        # TODO: guard: if self.cart.is_empty(): raise or return ("", "Cart is empty")
        # TODO: addr_errors = address.validate(); if any -> return ("", first_error or join)
        # TODO: subtotal, shipping, total = self.compute_totals(address)

        # Create order in 'pending' state
        # TODO: order = self.order_factory.create_from_cart(self.cart, address, shipping)
        # TODO: sanity: assert order.total == total (or set it during creation)

        # Take payment
        # TODO: success, message = self.payment_service.charge(order.id, total)

        # On success: mark paid, clear cart, optionally save address to account
        # TODO: if success:
        #           order.mark_paid()
        #           self.cart.clear()
        #           if save_to_account and self.account_service:
        #               self._try_save_default_address(address)
        #           return (order.id, message or "Payment processed")
        # TODO: else:
        #           return (order.id, message or "Payment failed")
        raise NotImplementedError

    # ----- Optional convenience -----
    def _try_save_default_address(self, address):
        """Optional: save to user account if an AccountService is wired in.
        Not implemented in this minimal build."""
        if self.account_service:
            # TODO: implement when AccountService exists
            pass