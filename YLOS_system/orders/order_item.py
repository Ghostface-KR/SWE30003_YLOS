"""
OrderItem - Represents a single line item in an order
Member 3 responsibility
Complexity: Simple (Data Holder)
"""

from decimal import Decimal


class OrderItem:
    """
    Immutable snapshot of a product at the time of order placement.
    Similar to CartItem but represents a confirmed purchase.
    """

    def __init__(self, product_id: str, name: str, unit_price: Decimal, qty: int) -> None:
        """
        Initialize an order item.
        
        Args:
            product_id: Product identifier
            name: Product name (snapshot at order time)
            unit_price: Price per unit (snapshot at order time)
            qty: Quantity ordered
            
        TODO:
        - Validate product_id is non-empty string
        - Validate name is non-empty string
        - Validate unit_price is Decimal and non-negative
        - Validate qty is int and positive (>= 1)
        - Store all as private attributes for read-only access
        - Convert unit_price to Decimal if needed
        """
        pass

    @property
    def product_id(self) -> str:
        """
        Read-only access to product ID.
        
        TODO:
        - Return the stored product_id
        """
        pass

    @property
    def name(self) -> str:
        """
        Read-only access to product name.
        
        TODO:
        - Return the stored name
        """
        pass

    @property
    def unit_price(self) -> Decimal:
        """
        Read-only access to unit price.
        
        TODO:
        - Return the stored unit_price
        """
        pass

    @property
    def qty(self) -> int:
        """
        Read-only access to quantity.
        
        TODO:
        - Return the stored qty
        """
        pass

    def subtotal(self) -> Decimal:
        """
        Calculate line item total.
        
        Returns:
            unit_price * qty
            
        TODO:
        - Multiply unit_price by qty
        - Return the result as Decimal
        """
        pass

    def to_dict(self) -> dict:
        """
        Convert to dictionary format.
        
        Returns:
            Dictionary with item details
            
        TODO:
        - Create dictionary with keys: 'product_id', 'name', 'unit_price', 'qty', 'subtotal'
        - Include calculated subtotal
        - Return the dictionary
        """
        pass

    # Methods that would be implemented in full system:
    # - with_qty(new_qty: int) -> OrderItem  # Not needed for orders (immutable after creation)
    # - equals(other: OrderItem) -> bool  # For comparison
