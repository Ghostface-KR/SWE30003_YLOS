"""
Address - Stores and validates customer delivery address
Member 2 responsibility (swapped with Member 3)
Complexity: Simple (Data Holder with validation)
"""

from typing import Optional, List


class Address:
    """
    Data holder for delivery address information with validation.
    Used in checkout process to determine shipping and delivery.
    """

    def __init__(self, street: str, city: str, state: str, postcode: str) -> None:
        """
        Initialize an address.
        
        Args:
            street: Street address (e.g., "123 Main St")
            city: City/suburb name
            state: State abbreviation (e.g., "VIC", "NSW")
            postcode: Postal code (4 digits for Australia)
            
        TODO:
        - Store all fields as private attributes
        - No validation in constructor (validation happens via validate() method)
        - Store raw input values even if potentially invalid
        """
        pass

    @property
    def street(self) -> str:
        """
        Read-only access to street address.
        
        TODO:
        - Return the stored street value
        """
        pass

    @property
    def city(self) -> str:
        """
        Read-only access to city.
        
        TODO:
        - Return the stored city value
        """
        pass

    @property
    def state(self) -> str:
        """
        Read-only access to state.
        
        TODO:
        - Return the stored state value
        """
        pass

    @property
    def postcode(self) -> str:
        """
        Read-only access to postcode.
        
        TODO:
        - Return the stored postcode value
        """
        pass

    def validate(self) -> Optional[str]:
        """
        Validate address completeness and format.
        Called by CheckoutService before processing order.
        
        Returns:
            None if valid, error message string if invalid
            
        TODO:
        - Check street is not empty string after stripping whitespace
        - Check city is not empty string after stripping whitespace
        - Check state is not empty string after stripping whitespace
        - Check postcode is exactly 4 digits (Australian format)
        - Return None if all validations pass
        - Return descriptive error message string if any validation fails
        - Example errors: "Street address required", "Postcode must be 4 digits"
        """
        pass

    def format(self) -> str:
        """
        Format address as single display string.
        
        Returns:
            Formatted address string
            
        TODO:
        - Combine all fields into readable format
        - Example: "123 Main St, Melbourne, VIC 3000"
        - Return the formatted string
        """
        pass

    def to_dict(self) -> dict:
        """
        Convert address to dictionary format for storage/serialization.
        
        Returns:
            Dictionary with address fields
            
        TODO:
        - Create dictionary with keys: 'street', 'city', 'state', 'postcode'
        - Return the dictionary
        """
        pass

    # Methods that would be implemented in full system:
    # - is_metro() -> bool  # Check if address is in metro area for shipping
    # - get_region() -> str  # Determine delivery region
    # - validate_deliverable() -> bool  # Check if address is in delivery range
