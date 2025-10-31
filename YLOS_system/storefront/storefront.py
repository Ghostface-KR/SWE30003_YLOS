"""
StoreFront - Facade coordinating customer-facing operations
Member 3 responsibility
Complexity: Medium
"""

from typing import List, Dict, Any, Tuple, Optional
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
        
        Args:
            catalogue: Catalogue instance for product operations
            cart: Cart instance for shopping cart operations
            checkout_service: CheckoutService instance for order processing
            
        TODO:
        - Store all collaborators as private attributes
        - Do not expose these as properties (encapsulation)
        - Validate that required collaborators are provided
        """
        pass

    # ----- Product Browsing (delegates to Catalogue) -----

    def browse_products(self) -> List[Dict[str, Any]]:
        """
        Browse all available products.
        Used in Scenario 2.
        
        Returns:
            List of product dictionaries
            
        TODO:
        - Delegate to catalogue.get_all_products()
        - Return the result directly
        - No additional logic needed (pure delegation)
        """
        pass

    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for products by keyword.
        Used in Scenario 2.
        
        Args:
            query: Search term
            
        Returns:
            List of matching products
            
        TODO:
        - Delegate to catalogue.search_products(query)
        - Return the result
        - Consider handling empty query (return all or empty list)
        """
        pass

    def filter_products_by_category(self, type_id: str) -> List[Dict[str, Any]]:
        """
        Filter products by category.
        Used in Scenario 2.
        
        Args:
            type_id: Product type to filter by
            
        Returns:
            List of products in category
            
        TODO:
        - Delegate to catalogue.filter_by_type(type_id)
        - Return the result
        """
        pass

    # ----- Cart Operations (delegates to Cart) -----

    def add_to_cart(self, product_id: str, qty: int = 1) -> None:
        """
        Add product to shopping cart.
        Used in Scenario 2.
        
        Args:
            product_id: Product to add
            qty: Quantity to add
            
        TODO:
        - Delegate to cart.add(product_id, qty)
        - Let Cart handle all validation and errors
        - No additional logic needed
        """
        pass

    def view_cart(self) -> Tuple[List[Dict[str, Any]], Decimal]:
        """
        View current cart contents and total.
        Used in Scenarios 2 and 3.
        
        Returns:
            Tuple of (list of cart items as dicts, subtotal)
            
        TODO:
        - Get cart items via cart.items()
        - Convert each CartItem to dictionary format with keys: 'product_id', 'name', 'unit_price', 'qty', 'subtotal'
        - Get subtotal via cart.subtotal()
        - Return tuple of (items_list, subtotal)
        """
        pass

    def update_cart_quantity(self, product_id: str, qty: int) -> None:
        """
        Update quantity of item in cart.
        Used in Scenario 2.
        
        Args:
            product_id: Product to update
            qty: New quantity (0 to remove)
            
        TODO:
        - Delegate to cart.update_qty(product_id, qty)
        - Let Cart handle validation and removal logic
        """
        pass

    def remove_from_cart(self, product_id: str) -> None:
        """
        Remove item from cart entirely.
        Used in Scenario 2.
        
        Args:
            product_id: Product to remove
            
        TODO:
        - Delegate to cart.remove(product_id)
        - Let Cart handle validation
        """
        pass

    # ----- Checkout (delegates to CheckoutService) -----

    def proceed_to_checkout(self, street: str, city: str, state: str, postcode: str) -> Tuple[str, str]:
        """
        Process checkout with delivery address.
        Used in Scenario 3.
        
        Args:
            street: Street address
            city: City name
            state: State abbreviation
            postcode: Postal code
            
        Returns:
            Tuple of (order_id, message)
            
        TODO:
        - Create Address instance from parameters
        - Delegate to checkout_service.place_order(address)
        - Return the (order_id, message) tuple from place_order
        - Let CheckoutService handle all validation, payment, and cart clearing
        """
        pass

    # Methods that would be implemented in full system but not needed for scenarios:
    # - login(email: str, password: str) -> bool
    # - logout() -> None
    # - register_account(email: str, password: str, ...) -> None
    # - get_order_history() -> List[Dict]
    # - get_order_status(order_id: str) -> Dict
    # - cancel_order(order_id: str) -> bool
