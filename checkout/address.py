from dataclasses import dataclass

@dataclass(frozen=True)
class Address:
    street_number: str
    street_name: str
    city: str
    state: str
    postcode: str

    def validate(self) -> list[str]:
        errors: list[str] = []
        # TODO: require non-empty fields; simple 4-digit postcode check
        return errors

    def formatted(self) -> str:
        # TODO: return one-line formatted string
        raise NotImplementedError
