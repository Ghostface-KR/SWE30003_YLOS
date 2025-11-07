# run_smoke_tests.py
import os
from decimal import Decimal
from pathlib import Path
from .catalogue.catalogue import Catalogue
from .catalogue.product import Product
from .checkout.cart import Cart
from .checkout.checkout_service import CheckoutService
from .checkout.shipping_policy import ShippingPolicy
from .checkout.payment_service import PaymentService
from .storefront.storefront import StoreFront
from .checkout.address import Address


# ---- Fake gateways for deterministic results ----
class FakeGatewaySuccess:
    def charge(self, order_id: str, amount: Decimal):
        return True, f"Charged ${amount.quantize(Decimal('0.01'))}"


class FakeGatewayFail:
    def charge(self, order_id: str, amount: Decimal):
        return False, "Card declined"


def seed_catalogue(cat: Catalogue):
    # Clear file and add fresh products
    cat.products = []
    # Use Catalogue.add_product() which takes separate parameters
    cat.add_product("MILK1", "Milk", 3.50, 50, "Daily Essentials")
    cat.add_product("BRED1", "Bread", 4.20, 30, "Daily Essentials")
    cat.add_product("APPL1", "Apple", 1.10, 100, "Fruit")
    cat.save_to_file()


def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)


def test_browse_search_filter(store: StoreFront):
    products = store.browse_products()
    assert_true(len(products) >= 3, "Expected at least 3 products after seeding")
    assert_true("id" in products[0] and "product_id" in products[0], "Product ID fields missing")
    # Search (case-insensitive substring)
    results = store.search_products("app")
    assert_true(any(p["name"].lower() == "apple" for p in results), "Search for 'app' should find Apple")
    # Filter (case-insensitive equality)
    results = store.filter_products_by_category("daily essentials")
    names = {p["name"].lower() for p in results}
    assert_true({"milk", "bread"}.issubset(names), "Filter by Daily Essentials should return Milk & Bread")


def test_cart_ops(cart: Cart, cat: Catalogue):
    # Add 2 milks
    cart.add("MILK1", 2)
    # Check cart has items (use len(cart.items()) instead of count_items)
    assert_true(len(cart.items()) == 1, "Cart should have 1 line item")
    # Increase qty
    cart.update_qty("MILK1", 3)
    # Subtotal = 3 * 3.50 = 10.50
    expected = Decimal("10.50")
    assert_true(cart.subtotal() == expected, f"Expected subtotal {expected}, got {cart.subtotal()}")
    # Remove & re-add
    cart.remove("MILK1")
    assert_true(cart.is_empty(), "Cart should be empty after removal")
    cart.add("APPL1", 5)  # 5 * 1.10 = 5.50
    assert_true(cart.subtotal() == Decimal("5.50"), "Apple subtotal should be 5.50")


def test_checkout_success(cat: Catalogue):
    cart = Cart(cat)
    cart.add("MILK1", 2)  # 2 * 3.50 = 7.00
    shipping = ShippingPolicy(Decimal("7.50"))
    checkout = CheckoutService(cart, shipping, PaymentService(FakeGatewaySuccess()))
    store = StoreFront(cat, cart, checkout)

    order_id, msg = store.proceed_to_checkout("1 Test St", "Bundoora", "VIC", "3083")
    assert_true(order_id and isinstance(order_id, str), "Order ID should be a non-empty string")
    assert_true(msg.startswith("Payment of $"), "Success message not standardized")
    # Cart cleared on success
    assert_true(cart.is_empty(), "Cart should be cleared after successful payment")


def test_checkout_failure(cat: Catalogue):
    cart = Cart(cat)
    cart.add("BRED1", 1)  # 4.20
    shipping = ShippingPolicy(Decimal("7.50"))
    checkout = CheckoutService(cart, shipping, PaymentService(FakeGatewayFail()))
    store = StoreFront(cat, cart, checkout)

    order_id, msg = store.proceed_to_checkout("1 Test St", "Bundoora", "VIC", "3083")
    assert_true(order_id and isinstance(order_id, str), "Order ID should be a non-empty string")
    assert_true(msg.startswith("Payment failed:"), "Failure message not standardized")
    # Cart NOT cleared on failure
    assert_true(not cart.is_empty(), "Cart should NOT be cleared after failed payment")


def main():
    # Use an isolated test data file so we don't touch real data
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    test_file = data_dir / "products_test.json"

    cat = Catalogue(data_file=str(test_file))
    seed_catalogue(cat)

    cart = Cart(cat)
    checkout = CheckoutService(cart, ShippingPolicy(Decimal("7.50")), PaymentService(FakeGatewaySuccess()))
    store = StoreFront(cat, cart, checkout)

    # Run tests
    print("Running smoke tests...")
    test_browse_search_filter(store)
    test_cart_ops(cart, cat)
    test_checkout_success(cat)
    test_checkout_failure(cat)
    print("✅ ALL TESTS PASSED")


if __name__ == "__main__":
    main()

# Run with: python3 -m YLOS_system.run_smoke_tests