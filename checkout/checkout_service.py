from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple

@dataclass
class CheckoutService:
    cart: object
    shipping_policy: object
    payment_service: object
    order_factory: object
    account_service: object | None = None

    def compute_totals(self, address: object) -> Tuple[Decimal, Decimal, Decimal]:
        # TODO: validate cart & address; compute subtotal, shipping, total
        raise NotImplementedError

    def place_order(self, address: object, save_to_account: bool = False) -> Tuple[str, str]:
        # TODO: create pending Order from cart, charge via PaymentService;
        # on success: order.mark_paid(), cart.clear(), optionally save address
        raise NotImplementedError
