"""
Shared Protocol definitions for dependency injection and loose coupling.
Protocols define interfaces without requiring inheritance.
"""

from typing import Protocol, Dict, Any, Tuple, List, Optional
from decimal import Decimal


class CataloguePort(Protocol):
    """
    Interface for catalogue operations required by Cart.
    Allows Cart to look up current product information when adding items.
    """

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve product information.

        Returns:
            Optional dictionary with keys: 'name', 'price', 'stock', 'category'
            Returns None if product not found
        """
        ...


class CartPort(Protocol):
    """
    Interface for cart operations required by ShippingPolicy and CheckoutService.
    Provides read-only access to cart state.
    """
    
    def subtotal(self) -> Decimal:
        """Calculate cart subtotal (before shipping/tax)."""
        ...
    
    def items(self) -> List[Any]:
        """Return list of cart items."""
        ...
    
    def is_empty(self) -> bool:
        """Check if cart has no items."""
        ...


class PaymentGatewayPort(Protocol):
    """
    Interface for external payment gateway integration.
    PaymentService delegates to implementations of this protocol.
    """
    
    def charge(self, order_id: str, amount: Decimal) -> Tuple[bool, str]:
        """
        Attempt to charge payment.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        ...


class LoggerPort(Protocol):
    """
    Interface for logging operations.
    Allows services to log events without depending on specific logging implementation.
    """
    
    def log(self, action: str, payload: Dict[str, Any]) -> None:
        """
        Log an event with structured data.
        
        Args:
            action: Event type/name
            payload: Event data as dictionary
        """
        ...


# Additional protocols that might be needed for full system:
# class NotificationPort(Protocol):
# class CourierPort(Protocol):