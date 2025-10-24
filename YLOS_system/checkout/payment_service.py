from decimal import Decimal
from typing import Tuple

class PaymentService:
    def charge(self, order_id: str, amount: Decimal) -> Tuple[bool, str]:
        # TODO: simulate payment success for demo
        return True, f"Payment of ${amount} processed. Order {order_id} confirmed"
