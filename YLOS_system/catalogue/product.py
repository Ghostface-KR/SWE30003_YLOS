"""
Product - Represents an individual product entity
Member 1 responsibility
Complexity: Simple (Data Holder)
"""

from decimal import Decimal
from typing import Optional


class Product:
    """
    Data holder representing a product with its attributes.
    Immutable once created to ensure data integrity.
    """

    def __init__(self, product_id: str, name: str, price: Decimal, stock: int, type_id: str) -> None:
        """
        Initialize a product.
        
        Args:
            product_id: Unique identifier
            name: Product name
            price: Unit price
            stock: Available quantity
            type_id: Reference to ProductType
            
        TODO:
        - Validate product_id is non-empty string
        - Validate name is non-empty string
        - Validate price is Decimal and positive
        - Validate stock is int and non-negative
        - Validate type_id is non-empty string
        - Store all attributes as private/read-only
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
    def price(self) -> Decimal:
        """
        Read-only access to product price.
        
        TODO:
        - Return the stored price as Decimal
        """
        pass

    @property
    def stock(self) -> int:
        """
        Read-only access to stock level.
        
        TODO:
        - Return the stored stock quantity
        """
        pass

    @property
    def type_id(self) -> str:
        """
        Read-only access to product type reference.
        
        TODO:
        - Return the stored type_id
        """
        pass

    def to_dict(self) -> dict:
        """
        Convert product to dictionary format for Catalogue operations.
        
        Returns:
            Dictionary with product attributes
            
        TODO:
        - Create dictionary with keys: 'id', 'name', 'price', 'stock', 'type_id'
        - Ensure price is included as Decimal or float
        - Return the dictionary
        """
        pass

    # Methods that would be implemented in full system:
    # - with_stock(new_stock: int) -> Product  # Return new Product instance with updated stock (immutability)
    # - with_price(new_price: Decimal) -> Product  # Return new Product instance with updated price
    # - is_available() -> bool  # Check if stock > 0
