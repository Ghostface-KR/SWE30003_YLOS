"""
ProductType - Represents a product category/classification
Member 1 responsibility
Complexity: Simple (Data Holder)
"""

from typing import Optional


class ProductType:
    """
    Data holder for product type/category information.
    Used for organizing and filtering products.
    """

    def __init__(self, type_id: str, name: str, description: Optional[str] = None) -> None:
        """
        Initialize a product type.
        
        Args:
            type_id: Unique identifier for this type
            name: Display name (e.g., "Daily Essentials", "Specialty Items")
            description: Optional description of this category

        TODO:
        - Validate type_id is non-empty string
        - Validate name is non-empty string
        - Store description (can be None or empty)
        - Store all attributes as private/read-only
        """
        pass

    @property
    def type_id(self) -> str:
        """
        Read-only access to type ID.

        TODO:
        - Return the stored type_id
        """
        pass

    @property
    def name(self) -> str:
        """
        Read-only access to type name.

        TODO:
        - Return the stored name
        """
        pass

    @property
    def description(self) -> Optional[str]:
        """
        Read-only access to type description.

        TODO:
        - Return the stored description (may be None)
        """
        pass

    def to_dict(self) -> dict:
        """
        Convert to dictionary format.

        Returns:
            Dictionary with type attributes

        TODO:
        - Create dictionary with keys: 'id', 'name', 'description'
        - Return the dictionary
        """
        pass

    # Methods that would be implemented in full system:
    # - Common product types could be pre-defined as class constants
    # - DAILY_ESSENTIALS = ProductType("daily", "Daily Essentials", "...")
    # - SPECIALTY_ITEMS = ProductType("specialty", "Specialty Items", "...")