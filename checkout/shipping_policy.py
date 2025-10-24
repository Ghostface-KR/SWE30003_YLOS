from decimal import Decimal

class ShippingPolicy:
    def cost_for(self, cart: object, address: object) -> Decimal:
        # TODO: compute shipping (flat rate for demo)
        return Decimal("0.00")
