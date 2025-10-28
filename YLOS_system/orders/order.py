"""
Order - Represents a confirmed purchase order
Member 3 responsibility
Complexity: Medium
"""

from decimal import Decimal
from typing import List
import datetime


class Order:
    """
    Represents a customer order with items, delivery details, and status tracking.
    Created by CheckoutService; status updated through order lifecycle.
    """

    def __init__(self, id: str, items: List[Any], address: Any, 
                 shipping: Decimal, total: Decimal, status: str = "PENDING") -> None:
        """
        Initialize an order.
        
        Args:
            id: Unique order identifier
            items: List of OrderItem instances
            address: Address instance for delivery
            shipping: Shipping cost
            total: Grand total (subtotal + shipping)
            status: Order status (default "PENDING")
            
        TODO:
        - Validate id is non-empty string
        - Validate items is non-empty list
        - Validate address is provided
        - Validate shipping is Decimal and non-negative
        - Validate total is Decimal and positive
        - Validate status is valid string (PENDING, PAID, FULFILLED, etc.)
        - Store all as private attributes
        - Store creation timestamp (datetime.now())
        - Initialize paid_at as None (set when marked paid)
        """
        pass

    @property
    def id(self) -> str:
        """
        Read-only access to order ID.
        
        TODO:
        - Return the stored id
        """
        pass

    @property
    def items(self) -> List[Any]:
        """
        Read-only access to order items.
        
        Returns:
            Copy of items list to prevent external modification
            
        TODO:
        - Return a copy of the items list (not the original reference)
        """
        pass

    @property
    def address(self) -> Any:
        """
        Read-only access to delivery address.
        
        TODO:
        - Return the stored address
        """
        pass

    @property
    def shipping(self) -> Decimal:
        """
        Read-only access to shipping cost.
        
        TODO:
        - Return the stored shipping amount
        """
        pass

    @property
    def total(self) -> Decimal:
        """
        Read-only access to order total.
        
        TODO:
        - Return the stored total amount
        """
        pass

    @property
    def status(self) -> str:
        """
        Read-only access to order status.
        
        TODO:
        - Return the current status
        """
        pass

    @property
    def created_at(self) -> datetime.datetime:
        """
        Read-only access to creation timestamp.
        
        TODO:
        - Return the stored creation timestamp
        """
        pass

    @property
    def paid_at(self) -> datetime.datetime:
        """
        Read-only access to payment timestamp.
        
        Returns:
            Timestamp when order was paid, or None if not yet paid
            
        TODO:
        - Return the stored paid_at timestamp (may be None)
        """
        pass

    def mark_paid(self) -> None:
        """
        Mark order as paid and record timestamp.
        Called by CheckoutService after successful payment.
        Used in Scenario 3.
        
        TODO:
        - Validate current status is "PENDING" (cannot pay twice)
        - Update status to "PAID"
        - Set paid_at to current timestamp (datetime.now())
        - Raise ValueError if order is not in PENDING status
        """
        pass

    def calculate_subtotal(self) -> Decimal:
        """
        Calculate subtotal from order items.
        
        Returns:
            Sum of all item subtotals
            
        TODO:
        - Iterate through all items
        - Sum up item.unit_price * item.qty for each item
        - Return the total as Decimal
        """
        pass

    def to_dict(self) -> dict:
        """
        Convert order to dictionary format for display/storage.
        
        Returns:
            Dictionary with order details
            
        TODO:
        - Create dictionary with keys: 'id', 'items', 'address', 'shipping', 'total', 'status', 'created_at', 'paid_at'
        - Convert items to list of dicts (call to_dict on each OrderItem)
        - Convert address to dict format
        - Convert timestamps to ISO format strings
        - Return the dictionary
        """
        pass

    # Methods that would be implemented in full system:
    # - mark_fulfilled() -> None
    # - mark_shipped(tracking_number: str) -> None
    # - mark_delivered() -> None
    # - cancel() -> None
    # - add_tracking(tracking_number: str, carrier: str) -> None
    # - Valid status transitions would be enforced (state machine pattern)
