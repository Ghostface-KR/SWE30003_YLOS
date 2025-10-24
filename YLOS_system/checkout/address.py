from dataclasses import dataclass

@dataclass(frozen=True)
class Address:
    """
    Simple value object for shipping address.
    Keep it immutable; validate on use.
    """
    street_number: str
    street_name: str
    city: str
    state: str
    postcode: str  # expect 4 digits (AU), but keep generic

    def validate(self) -> list[str]:
        """
        Return a list of problems; empty list means it's valid.
        """
        errors: list[str] = []
        # TODO: trim whitespace on each field when checking
        # TODO: require all fields non-empty
        # TODO: simple postcode rule (e.g., digits only, length 4) for VIC demo
        # TODO: (optional) normalize state (uppercase)
        return errors

    def formatted(self) -> str:
        """
        Nicely formatted single-line address for receipts/labels.
        """
        # TODO: return f"{self.street_number} {self.street_name}, {self.city} {self.state} {self.postcode}"
        raise NotImplementedError

    def normalized(self) -> "Address":
        """
        Return a normalized copy (trimmed fields, uppercase state).
        """
        # TODO: build and return a new Address with normalized fields
        raise NotImplementedError