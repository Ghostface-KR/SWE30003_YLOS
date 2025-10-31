"""
Catalogue - Provides product listings and search functionality
Member 1 responsibility
Complexity: Complex
"""

from typing import List, Optional, Dict, Any


class Catalogue:
    """
    Manages the product catalogue with search, filter, and browse capabilities.
    Provides read-only access to product information for customers.
    """

    def __init__(self) -> None:
        """
        Initialize the catalogue.
        
        TODO:
        - Create internal storage for products (e.g., dictionary with product_id as key)
        - Initialize any indexing structures for efficient search/filtering
        - Consider loading initial product data if needed
        """
        pass

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single product by its ID.
        Used by Cart when adding items to capture current price/name/stock.
        
        Args:
            product_id: Unique identifier for the product
            
        Returns:
            Dictionary containing product data with keys: 'name', 'price', 'stock', 'type_id'
            Returns None if product not found
            
        TODO:
        - Validate product_id is not empty
        - Look up product in internal storage
        - Return dictionary with all required fields or None if not found
        - Ensure returned dict has correct types (str name, Decimal/float price, int stock)
        """
        pass

    def get_all_products(self) -> List[Dict[str, Any]]:
        """
        Retrieve all products in the catalogue.
        Used for browsing and admin product list display.
        
        Returns:
            List of product dictionaries
            
        TODO:
        - Return a copy/list of all products from internal storage
        - Ensure customers cannot modify the catalogue through returned references
        - Consider filtering out products with stock=0 or marking them clearly
        """
        pass

    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for products by keyword in name or description.
        
        Args:
            query: Search term to match against product names
            
        Returns:
            List of matching product dictionaries
            
        TODO:
        - Validate query is not empty (or return all products if empty)
        - Perform case-insensitive search in product names
        - Return list of matching products
        - Consider returning empty list vs all products for empty query
        """
        pass

    def filter_by_type(self, type_id: str) -> List[Dict[str, Any]]:
        """
        Filter products by their product type/category.
        
        Args:
            type_id: The product type identifier to filter by
            
        Returns:
            List of products matching the specified type
            
        TODO:
        - Validate type_id exists
        - Filter products that match the given type_id
        - Return filtered list
        - Handle case where type_id doesn't exist (empty list or error)
        """
        pass

    def add_type(self, type_id: str, name: str, description: Optional[str] = None) -> None:
        """
        Register a product type/category in the catalogue.

        Args:
            type_id: Canonical identifier (e.g., "dairy").
            name: Human‑readable name (e.g., "Dairy").
            description: Optional longer description for menus/help.

        Raises:
            ValueError: If validation fails (e.g., empty fields or duplicate type_id).

        TODO:
        - Ensure an internal type registry exists (e.g., self._types: Dict[str, Dict[str, str]])
          and is initialized in __init__ if not already.
        - Validate inputs: non‑empty strings for type_id and name; consider length/character rules.
        - Enforce uniqueness of type_id (consider case‑insensitive comparison).
        - Store in registry, e.g.: self._types[type_id] = {"name": name, "description": description or ""}.
        - Consider exposing helper methods later (has_type, get_all_types) for validation/UI lists.
        """
        pass

    # Admin operations (used in Scenario 1 and 4)
    
    def add_product(self, product_id: str, name: str, price: float, stock: int, type_id: str) -> None:
        """
        Add a new product to the catalogue (admin operation).
        
        Args:
            product_id: Unique identifier for the product
            name: Product name
            price: Product price (must be positive)
            stock: Available stock quantity (must be non-negative)
            type_id: Associated product type
            
        Raises:
            ValueError: If validation fails
            
        TODO:
        - Validate all inputs (non-empty strings, positive price, non-negative stock)
        - Check product_id doesn't already exist
        - Validate type_id exists (depends on ProductType class)
        - Add product to internal storage
        - Consider logging or notifying of catalogue changes
        """
        pass

    def update_product(self, product_id: str, name: Optional[str] = None, 
                      price: Optional[float] = None, stock: Optional[int] = None) -> None:
        """
        Update an existing product's details (admin operation).
        
        Args:
            product_id: Product to update
            name: New name (if provided)
            price: New price (if provided)
            stock: New stock level (if provided)
            
        Raises:
            ValueError: If product not found or validation fails
            
        TODO:
        - Validate product exists
        - Validate any provided fields (positive price, non-negative stock)
        - Update only the fields that are provided (not None)
        - Keep existing values for fields not provided
        """
        pass

    def delete_product(self, product_id: str) -> None:
        """
        Remove a product from the catalogue (admin operation).
        
        Args:
            product_id: Product to delete
            
        Raises:
            ValueError: If product not found
            
        TODO:
        - Validate product exists
        - Remove product from internal storage
        - Consider soft-delete vs hard-delete for order history integrity
        - Handle case where product is in active carts/orders
        """
        pass

    # Methods that would be implemented in full system but not needed for scenarios:
    # - get_products_by_ids(product_ids: List[str]) -> List[Dict]
    # - update_stock(product_id: str, quantity_delta: int) -> None
    # - get_low_stock_products(threshold: int) -> List[Dict]
    # - search_with_filters(query: str, type_id: Optional[str], min_price: Optional[float], max_price: Optional[float]) -> List[Dict]
