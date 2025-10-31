from decimal import Decimal
from typing import Dict, List, Optional, Callable, Any
import datetime

class Cart:
    """
    Holds CartItem snapshots (id, name, unit_price, qty).
    Fetches current product info from a Catalogue ONLY when adding items.
    After that, prices come from the CartItems (snapshots).
    """

    def __init__(self, catalogue: CataloguePort, logger: Optional[Callable[[str, dict], None]] = None) -> None:
        self._catalogue = catalogue     # internal reference to a port (get_product)
        self._logger = logger
        self._items: Dict[str, "CartItem"] = {}  # internal storage: product_id -> CartItem

    def _log(self, action: str, **fields) -> None:
        if not hasattr(self, "_logger") or self._logger is None:
            return
        payload = {"timestamp": datetime.datetime.now().isoformat(), "action": action}
        payload.update(fields)
        try:
            self._logger(action, payload)
        except Exception:
            # Swallow logger errors to avoid breaking domain logic
            pass

    # ----- Queries -----
    def items(self) -> List["CartItem"]:
        """Return a list of current CartItems (read-only copy)."""
        return list(self._items.values())


    def subtotal(self) -> Decimal:
        """Sum of line subtotals (no shipping or tax)."""
        return sum((item.subtotal() for item in self._items.values()), Decimal("0.00"))


    def is_empty(self) -> bool:
        """True if the cart has no items."""
        return len(self._items) == 0

    # ----- Commands -----
    def add(self, product_id: str, qty: int = 1) -> None:
        """
        Add a product (creates/updates a CartItem snapshot with current name & price).
        """
        # Validates qty is int & >= 1
        if isinstance(qty, bool):
            raise ValueError("qty must be an integer, not a boolean")
        if not isinstance(qty, int):
            raise ValueError("qty must be an integer")
        if qty < 1:
            raise ValueError("qty must be ≥ 1")

        # Lookup product via catalogue, validate not empty
        fetch = self._catalogue.get_product(product_id)
        if fetch is None:
            raise ValueError("product not found in catalogue")

        # Extract fields from the catalogue record (read-only) w/ validation
        if "name" not in fetch:
            raise KeyError("product 'name' missing")
        name = fetch["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("invalid product name")

        if "price" not in fetch:
            raise KeyError("product 'price' missing")
        price = fetch["price"]
        if not isinstance(price, (int, float, Decimal)):
            raise TypeError("product price must be a number")
        if price < 0:
            raise ValueError("product price cannot be negative")

        if "stock" not in fetch:
            raise KeyError("product 'stock' missing")
        stock = fetch["stock"]
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("invalid product stock")


        # Determine the intended new quantity and ensure available stock is sufficient
        if product_id in self._items:
            existing_qty = self._items[product_id].qty
        else:
            existing_qty = 0

        intended_qty = existing_qty + qty

        if intended_qty > stock:
            raise ValueError(f"only {stock} left in stock")

        # Choose correct unit price snapshot (keep existing price if already in cart)
        if product_id in self._items:
            unit_price_snapshot = self._items[product_id].unit_price
        else:
            unit_price_snapshot = Decimal(str(price))

        # Build updated CartItem (immutable)
        if product_id in self._items:
            old_item = self._items[product_id]
            new_item = old_item.with_qty(intended_qty)
        else:
            new_item = CartItem(product_id, name, unit_price_snapshot, intended_qty)

        # Save new/updated line to cart
        self._items[product_id] = new_item


        # Log cart changes for traceability and analytics
        self._log("add/update", product_id=product_id, qty=qty, new_total_qty=intended_qty)

    def update_qty(self, product_id: str, qty: int) -> None:
        """
        Set a new quantity for an item; remove if qty == 0.
        """
        # Check if product is in cart.
        if product_id not in self._items:
            raise ValueError("product not found in cart")

        # Removes product if qty is 0
        if qty == 0:
            self.remove(product_id)
            return

        # Validates that the requested quantity is an integer and at least 1.
        if isinstance(qty, bool):
            raise ValueError("qty must be an integer, not a boolean")
        if not isinstance(qty, int):
            raise ValueError("qty must be an integer")
        if qty < 1:
            raise ValueError("qty must be ≥ 1")

        # Early return: no change needed if requested qty equals current qty
        existing_qty = self._items[product_id].qty
        if qty == existing_qty:
            return

        # Determine if this update increases the required stock; only then consult the catalogue
        if qty > existing_qty:
            # Lookup product via catalogue, validate not empty
            fetch = self._catalogue.get_product(product_id)
            if fetch is None:
                raise ValueError("product not found in catalogue")

            # Read and validate stock only (name/price not needed for qty updates)
            if "stock" not in fetch:
                raise KeyError("product 'stock' missing")
            stock = fetch["stock"]
            if not isinstance(stock, int) or stock < 0:
                raise ValueError("invalid product stock")

            # Compare requested quantity to available stock
            if qty > stock:
                raise ValueError(f"only {stock} left in stock")
        else:
            # qty <= existing; no stock increase needed; no catalogue call required
            pass

        # Replace the existing cart line immutably with the updated quantity (keep price snapshot)
        old_item = self._items[product_id]
        new_item = old_item.with_qty(qty)
        self._items[product_id] = new_item

        # Optional: log this quantity change for traceability (simple stdout log)
        self._log("update_qty", product_id=product_id, old_qty=existing_qty, new_qty=qty)

    def remove(self, product_id: str) -> None:
        """Remove an item entirely."""

        if product_id not in self._items:
            raise ValueError("product not found in cart")

        del self._items[product_id]

        # Log removal for traceability
        self._log("remove", product_id=product_id)

    def clear(self) -> None:
        """Empty the cart after a successful order."""
        self._items.clear()