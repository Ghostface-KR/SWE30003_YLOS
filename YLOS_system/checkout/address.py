"""
Address - Stores and validates customer delivery address
Member 2 responsibility (swapped with Member 3)
Complexity: Simple (Data Holder with validation)
"""

from typing import Optional


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
        """
        # Store all fields as private attributes without validation
        self._street = street
        self._city = city
        self._state = state
        self._postcode = postcode

    @property
    def street(self) -> str:
        """Read-only access to street address."""
        return self._street

    @property
    def city(self) -> str:
        """Read-only access to city."""
        return self._city

    @property
    def state(self) -> str:
        """Read-only access to state."""
        return self._state

    @property
    def postcode(self) -> str:
        """Read-only access to postcode."""
        return self._postcode

    def validate(self) -> Optional[str]:
        """
        Validate address completeness and format.
        Called by CheckoutService before processing order.

        Returns:
            None if valid, error message string if invalid
        """
        # Strip whitespace for checks
        street = (self._street or "").strip()
        city = (self._city or "").strip()
        state = (self._state or "").strip()
        postcode = (self._postcode or "").strip()

        if not street:
            return "Street address required"
        if not city:
            return "City required"
        if not state:
            return "State required"
        if not postcode:
            return "Postcode required"
        if not postcode.isdigit() or len(postcode) != 4:
            return "Postcode must be 4 digits"

        # Valid
        return None

    def format(self) -> str:
        """
        Format address as single display string.

        Returns:
            Formatted address string (e.g., "123 Main St, Melbourne, VIC 3000")
        """
        return f"{self._street}, {self._city}, {self._state} {self._postcode}"

    def to_dict(self) -> dict:
        """
        Convert address to dictionary format for storage/serialization.

        Returns:
            Dictionary with address fields
        """
        return {
            "street": self._street,
            "city": self._city,
            "state": self._state,
            "postcode": self._postcode
        }

    # Methods that would be implemented in full system:
    # - is_metro() -> bool  # Check if address is in metro area for shipping
    # - get_region() -> str  # Determine delivery region
    # - validate_deliverable() -> bool  # Check if address is in delivery range
