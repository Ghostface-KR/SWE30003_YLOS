"""
StoreFront - Facade coordinating customer-facing operations
Member 3 responsibility
Complexity: Medium
"""

from typing import List, Dict, Any, Tuple
from decimal import Decimal


class StoreFront:
    """
    Facade providing unified entry point for customer operations.
    Coordinates subsystems: Catalogue, Cart, CheckoutService.
    Simplifies client interaction by hiding subsystem complexity.
    """

    def __init__(self, catalogue: Any, cart: Any, checkout_service: Any) -> None:
        """
        Initialize the storefront with its subsystems.
        """
        if catalogue is None:
            raise ValueError("catalogue is required")
        if cart is None:
            raise ValueError("cart is required")
        if checkout_service is None:
            raise ValueError("checkout_service is required")

        # private collaborators (not exposed)
        self._catalogue = catalogue
        self._cart = cart
        self._checkout_service = checkout_service

    # ----- Product Browsing (delegates to Catalogue) -----

    def browse_products(self) -> List[Dict[str, Any]]:
        """
        Browse all available products.
        Used in Scenario 2.
        """
        return self._catalogue.get_all_products()

    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for products by keyword.
        Used in Scenario 2.
        """
        q = (query or "").strip()
        if not q:
            # reasonable behaviour: return all when query empty
            return self._catalogue.get_all_products()
        return self._catalogue.search_products(q)

    def filter_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Filter products by category.
        Used in Scenario 2.
        """
        return self._catalogue.filter_by_type(category)

    # ----- Cart Operations (delegates to Cart) -----

    def add_to_cart(self, product_id: str, qty: int = 1) -> None:
        """
        Add product to shopping cart.
        Used in Scenario 2.
        """
        self._cart.add(product_id, qty)

    def view_cart(self) -> Tuple[List[Dict[str, Any]], Decimal]:
        """
        View current cart contents and total.
        Used in Scenarios 2 and 3.
        """
        items_dicts: List[Dict[str, Any]] = []
        for ci in self._cart.items():
            # CartItem exposes properties and subtotal()
            items_dicts.append(
                {
                    "product_id": getattr(ci, "product_id"),
                    "name": getattr(ci, "name"),
                    "unit_price": getattr(ci, "unit_price"),
                    "qty": getattr(ci, "qty"),
                    "subtotal": ci.subtotal(),
                }
            )
        return items_dicts, self._cart.subtotal()

    def update_cart_quantity(self, product_id: str, qty: int) -> None:
        """
        Update quantity of item in cart.
        Used in Scenario 2.
        """
        self._cart.update_qty(product_id, qty)

    def remove_from_cart(self, product_id: str) -> None:
        """
        Remove item from cart entirely.
        Used in Scenario 2.
        """
        self._cart.remove(product_id)

    # ----- Checkout (delegates to CheckoutService) -----

    def proceed_to_checkout(self, street: str, city: str, state: str, postcode: str) -> Tuple[str, str]:
        """
        Process checkout with delivery address.
        Used in Scenario 3.
        """
        # local import to avoid circulars and keep module boundaries clean
        from YLOS_system.checkout.address import Address

        address = Address(street, city, state, postcode)
        return self._checkout_service.place_order(address)

    # Methods that would be implemented in full system but not needed for scenarios:
    # - login(email: str, password: str) -> bool
    # - logout() -> None
    # - register_account(email: str, password: str, ...) -> None
    # - get_order_history() -> List[Dict]
    # - get_order_status(order_id: str) -> Dict
    # - cancel_order(order_id: str) -> bool
