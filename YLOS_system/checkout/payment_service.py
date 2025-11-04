from decimal import Decimal
from typing import Tuple, Optional
from YLOS_system.protocols import PaymentGatewayPort

class PaymentService:
    """
    Minimal demo payment service.
    Keeps side-effects out; just returns a success/fail + message.
    """

    def __init__(self, gateway: Optional[PaymentGatewayPort] = None) -> None:
        self._gateway = gateway  # internal collaborator (optional)

    def charge(self, order_id: str, amount: Decimal) -> Tuple[bool, str]:
        """
        Attempt to charge the customer for the given order.
        Returns (success, message).
        """
        # Validate inputs
        if not isinstance(order_id, str) or not order_id.strip():
            return (False, "invalid order_id")
        if not isinstance(amount, Decimal):
            return (False, "amount must be a Decimal")
        if amount < Decimal("0.00"):
            return (False, "amount cannot be negative")

        # Optional: delegate to an injected gateway if available
        if self._gateway is not None and hasattr(self._gateway, "charge"):
            return self._gateway.charge(order_id, amount)

        # Minimal demo behavior: succeed without side effects
        return (True, f"Payment approved for order {order_id} amount {amount}")