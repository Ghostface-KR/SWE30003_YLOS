import uuid
import datetime
from decimal import Decimal
from typing import Tuple, Optional, Callable, Any

from order_item import OrderItem
from order import Order


from .cart import Cart           # uncomment when wiring
from .shipping_policy import ShippingPolicy
from .payment_service import PaymentService
from .address import Address


class CheckoutService:
    """
    Coordinates checkout steps (validate address, compute shipping/total,
    create order, request payment, finalize on success).
    Uses properties to expose collaborators read-only.
    """
    def __init__(
        self,
        cart: "Cart",
        shipping_policy: "ShippingPolicy",
        payment_service: "PaymentService",
    ) -> None:
        self._cart = cart
        self._shipping_policy = shipping_policy
        self._payment_service = payment_service


    def _log(self, action: str, **fields) -> None:
        if getattr(self, "_logger", None) is None:
            return
        payload = {"timestamp": datetime.datetime.now().isoformat(), "action": action}
        payload.update(fields)
        try:
            self._logger(action, payload)
        except Exception:
            pass

    # ----- Helper queries -----

    # Note: Address.validate() should return a falsy value when valid; any truthy value is treated as invalid.
    def compute_totals(self, address: "Address") -> Tuple[Decimal, Decimal, Decimal]:
        """
        Returns (subtotal, shipping, total).
        """
        # Ensure the cart isn't empty before calculating totals.
        if self._cart.is_empty():
            raise ValueError("Cart is empty")

        # Validate address; raise error if invalid.
        addr_errors = address.validate()
        if addr_errors:
            raise ValueError(f"Invalid address: {addr_errors}")

        # Get subtotal from all cart items.
        subtotal = self._cart.subtotal()

        # Get shipping cost from ShippingPolicy.
        shipping = self._shipping_policy.cost_for(self._cart, address)

        # Add subtotal and shipping to calculate total.
        total = subtotal + shipping
        if total < 0:
            raise ValueError("Total cannot be negative")

        self._log("compute_totals", subtotal=str(subtotal), shipping=str(shipping), total=str(total))
        return subtotal, shipping, total


    # ----- Main flow -----
    def place_order(
        self,
        address: "Address"
    ) -> Tuple[str, str]:
        """
        Validate address; compute shipping/total; create order (pending);
        take payment; on success mark paid + clear cart; return (order_id, message).
        """
        # Create a pending order snapshot using helper method.
        subtotal, shipping, total = self.compute_totals(address)

        order = self._create_order_from_cart(self._cart, address, shipping)
        self._log("order_created", order_id=getattr(order, "id", "<no-id>"))
        # Check totals match; show both expected and actual values for debugging.
        if order.total != total:
            self._log("order_total_mismatch", order_id=getattr(order, "id", "<no-id>"),
                      expected=str(total), actual=str(order.total))
            raise ValueError(
                f"Order total mismatch for order {order.id}: expected {total.quantize(Decimal('0.01'))}, got {order.total.quantize(Decimal('0.01'))}"
            )

        # Request payment and get (success, message) tuple.
        success, message = self._payment_service.charge(order.id, total)
        self._log("payment_attempt", order_id=order.id, amount=str(total), success=success, message=message)

        # Ensure charge() returns (bool, str); handle both outcomes.
        if not isinstance(success, bool) or not isinstance(message, str):
            raise TypeError("PaymentService.charge() must return (bool, str)")

        # Success path: mark paid, clear cart, then return
        if success:
            # Rely on Order's public interface only
            order.mark_paid()
            # Clear cart only after successful payment.
            self._cart.clear()
            self._log("payment_success", order_id=order.id)
            return (order.id, message)

        # Payment failed: keep order pending; return (order.id, message) for UI retry.
        self._log("payment_failed", order_id=order.id, message=message)

        return (order.id, message)

    # ----- Helper method to create order from cart -----
    def _create_order_from_cart(self, cart, address, shipping: Decimal) -> "Order":
        """
        Build and return a new Order object from the current cart snapshot.

        Steps:
        1) Generate unique order ID.
        2) Copy CartItems into OrderItems (snapshot, no references).
        3) Calculate subtotal and total (subtotal + shipping).
        4) Attach address and shipping.
        5) Set initial status to 'PENDING'.
        """
        # 1) ID
        order_id = uuid.uuid4().hex

        # 2) Copy cart items -> order items (snapshot)
        order_items: list[OrderItem] = []
        for item in cart.items():  # expect Cart.items() -> list of CartItem
            order_items.append(
                OrderItem(
                    product_id=item.product_id,
                    name=item.name,
                    unit_price=item.unit_price,
                    qty=item.qty,
                )
            )

        # 3) Money math (recompute here from items to avoid relying on cart state after)
        subtotal = sum((oi.unit_price * oi.qty for oi in order_items), Decimal("0.00"))
        total = subtotal + shipping

        # 4) Build Order (pending)
        order = Order(
            id=order_id,
            items=order_items,
            address=address,
            shipping=shipping,
            total=total,
            status="PENDING",
        )
        return order
