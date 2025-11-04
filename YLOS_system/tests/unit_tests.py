"""
test_ylos_system.py - Comprehensive Unit Tests for YLOS System

Tests all modules and their integrations:
- Product, ProductType, Address (Data Holders)
- Catalogue (Product Management)
- CartItem, Cart (Shopping Cart)
- OrderItem, Order (Order Management)
- ShippingPolicy, PaymentService (Business Logic)
- CheckoutService (Orchestration)
- StoreFront (Facade)

Run: python test_ylos_system.py
"""

import unittest
from decimal import Decimal
from typing import Dict, Any

# Import all modules to test
try:
    from product import Product
    from product_type import ProductType
    from address import Address
    from catalogue import Catalogue
    from cart_item import CartItem
    from cart import Cart
    from order_item import OrderItem
    from order import Order
    from shipping_policy import ShippingPolicy
    from payment_service import PaymentService
    from checkout_service import CheckoutService
    from storefront import StoreFront

    IMPORTS_OK = True
except ImportError as e:
    print(f"Import Error: {e}")
    IMPORTS_OK = False


# ========== DATA HOLDER TESTS ==========

class TestProduct(unittest.TestCase):
    """Test Product data holder."""

    def test_product_creation_valid(self):
        """Test creating a valid product."""
        product = Product("P1", "Milk", Decimal("3.50"), 20, "dairy")
        self.assertEqual(product.product_id, "P1")
        self.assertEqual(product.name, "Milk")
        self.assertEqual(product.price, Decimal("3.50"))
        self.assertEqual(product.stock, 20)
        self.assertEqual(product.type_id, "dairy")

    def test_product_to_dict(self):
        """Test product serialization to dict."""
        product = Product("P1", "Milk", Decimal("3.50"), 20, "dairy")
        result = product.to_dict()
        self.assertEqual(result["id"], "P1")
        self.assertEqual(result["name"], "Milk")
        self.assertEqual(result["price"], Decimal("3.50"))

    def test_product_invalid_price(self):
        """Test product creation with negative price fails."""
        with self.assertRaises(ValueError):
            Product("P1", "Milk", Decimal("-1.00"), 20, "dairy")

    def test_product_invalid_stock(self):
        """Test product creation with negative stock fails."""
        with self.assertRaises(ValueError):
            Product("P1", "Milk", Decimal("3.50"), -5, "dairy")

    def test_product_empty_id(self):
        """Test product creation with empty ID fails."""
        with self.assertRaises(ValueError):
            Product("", "Milk", Decimal("3.50"), 20, "dairy")


class TestProductType(unittest.TestCase):
    """Test ProductType data holder."""

    def test_producttype_creation_valid(self):
        """Test creating a valid product type."""
        ptype = ProductType("dairy", "Dairy Products", "Milk and cheese")
        self.assertEqual(ptype.type_id, "dairy")
        self.assertEqual(ptype.name, "Dairy Products")
        self.assertEqual(ptype.description, "Milk and cheese")

    def test_producttype_no_description(self):
        """Test product type without description."""
        ptype = ProductType("dairy", "Dairy Products")
        self.assertEqual(ptype.description, None)

    def test_producttype_to_dict(self):
        """Test product type serialization."""
        ptype = ProductType("dairy", "Dairy Products", "Test")
        result = ptype.to_dict()
        self.assertEqual(result["id"], "dairy")
        self.assertEqual(result["name"], "Dairy Products")

    def test_producttype_empty_id(self):
        """Test product type with empty ID fails."""
        with self.assertRaises(ValueError):
            ProductType("", "Dairy")


class TestAddress(unittest.TestCase):
    """Test Address data holder with validation."""

    def test_address_creation_valid(self):
        """Test creating a valid address."""
        addr = Address("123 Main St", "Melbourne", "VIC", "3000")
        self.assertEqual(addr.street, "123 Main St")
        self.assertEqual(addr.city, "Melbourne")
        self.assertEqual(addr.state, "VIC")
        self.assertEqual(addr.postcode, "3000")

    def test_address_validate_success(self):
        """Test valid address passes validation."""
        addr = Address("123 Main St", "Melbourne", "VIC", "3000")
        result = addr.validate()
        self.assertIsNone(result)

    def test_address_validate_empty_street(self):
        """Test address with empty street fails validation."""
        addr = Address("", "Melbourne", "VIC", "3000")
        result = addr.validate()
        self.assertIsNotNone(result)
        self.assertIn("Street", result)

    def test_address_validate_invalid_postcode(self):
        """Test address with invalid postcode fails validation."""
        addr = Address("123 Main St", "Melbourne", "VIC", "300")  # Only 3 digits
        result = addr.validate()
        self.assertIsNotNone(result)
        self.assertIn("4 digits", result)

    def test_address_format(self):
        """Test address formatting."""
        addr = Address("123 Main St", "Melbourne", "VIC", "3000")
        formatted = addr.format()
        self.assertEqual(formatted, "123 Main St, Melbourne, VIC 3000")

    def test_address_to_dict(self):
        """Test address serialization."""
        addr = Address("123 Main St", "Melbourne", "VIC", "3000")
        result = addr.to_dict()
        self.assertEqual(result["street"], "123 Main St")
        self.assertEqual(result["postcode"], "3000")


# ========== CATALOGUE TESTS ==========

class TestCatalogue(unittest.TestCase):
    """Test Catalogue product management."""

    def setUp(self):
        """Create fresh catalogue for each test."""
        self.catalogue = Catalogue()

    def test_catalogue_starts_empty(self):
        """Test new catalogue has no products."""
        products = self.catalogue.get_all_products()
        self.assertEqual(len(products), 0)

    def test_add_product_success(self):
        """Test adding a valid product."""
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        products = self.catalogue.get_all_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Milk")

    def test_add_duplicate_product_fails(self):
        """Test adding duplicate product ID fails."""
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        with self.assertRaises(ValueError):
            self.catalogue.add_product("P1", "Bread", 2.50, 10, "bakery")

    def test_get_product_exists(self):
        """Test retrieving existing product."""
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        product = self.catalogue.get_product("P1")
        self.assertIsNotNone(product)
        self.assertEqual(product["name"], "Milk")
        self.assertEqual(product["price"], 3.50)

    def test_get_product_not_exists(self):
        """Test retrieving non-existent product returns None."""
        product = self.catalogue.get_product("INVALID")
        self.assertIsNone(product)

    def test_update_product_name(self):
        """Test updating product name."""
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        self.catalogue.update_product("P1", name="Whole Milk")
        product = self.catalogue.get_product("P1")
        self.assertEqual(product["name"], "Whole Milk")

    def test_update_product_price(self):
        """Test updating product price."""
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        self.catalogue.update_product("P1", price=4.00)
        product = self.catalogue.get_product("P1")
        self.assertEqual(product["price"], 4.00)

    def test_update_product_stock(self):
        """Test updating product stock."""
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        self.catalogue.update_product("P1", stock=15)
        product = self.catalogue.get_product("P1")
        self.assertEqual(product["stock"], 15)

    def test_update_nonexistent_product_fails(self):
        """Test updating non-existent product fails."""
        with self.assertRaises(ValueError):
            self.catalogue.update_product("INVALID", name="Test")

    def test_delete_product_success(self):
        """Test deleting existing product."""
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        self.catalogue.delete_product("P1")
        products = self.catalogue.get_all_products()
        self.assertEqual(len(products), 0)

    def test_delete_nonexistent_product_fails(self):
        """Test deleting non-existent product fails."""
        with self.assertRaises(ValueError):
            self.catalogue.delete_product("INVALID")

    def test_search_products_found(self):
        """Test searching for products by keyword."""
        self.catalogue.add_product("P1", "Whole Milk", 3.50, 20, "dairy")
        self.catalogue.add_product("P2", "Skim Milk", 3.00, 15, "dairy")
        self.catalogue.add_product("P3", "Bread", 2.50, 10, "bakery")

        results = self.catalogue.search_products("milk")
        self.assertEqual(len(results), 2)

    def test_search_products_not_found(self):
        """Test searching with no matches."""
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        results = self.catalogue.search_products("chocolate")
        self.assertEqual(len(results), 0)

    def test_filter_by_type(self):
        """Test filtering products by category."""
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        self.catalogue.add_product("P2", "Cheese", 5.00, 10, "dairy")
        self.catalogue.add_product("P3", "Bread", 2.50, 15, "bakery")

        dairy_products = self.catalogue.filter_by_type("dairy")
        self.assertEqual(len(dairy_products), 2)


# ========== CART TESTS ==========

class TestCartItem(unittest.TestCase):
    """Test CartItem data holder."""

    def test_cartitem_creation_valid(self):
        """Test creating valid cart item."""
        item = CartItem("P1", "Milk", Decimal("3.50"), 2)
        self.assertEqual(item.product_id, "P1")
        self.assertEqual(item.name, "Milk")
        self.assertEqual(item.unit_price, Decimal("3.50"))
        self.assertEqual(item.qty, 2)

    def test_cartitem_subtotal(self):
        """Test cart item subtotal calculation."""
        item = CartItem("P1", "Milk", Decimal("3.50"), 2)
        self.assertEqual(item.subtotal(), Decimal("7.00"))

    def test_cartitem_with_qty(self):
        """Test creating new cart item with updated quantity."""
        item = CartItem("P1", "Milk", Decimal("3.50"), 2)
        new_item = item.with_qty(5)
        self.assertEqual(new_item.qty, 5)
        self.assertEqual(item.qty, 2)  # Original unchanged

    def test_cartitem_invalid_qty(self):
        """Test cart item with invalid quantity fails."""
        with self.assertRaises(ValueError):
            CartItem("P1", "Milk", Decimal("3.50"), 0)

    def test_cartitem_negative_price(self):
        """Test cart item with negative price fails."""
        with self.assertRaises(ValueError):
            CartItem("P1", "Milk", Decimal("-1.00"), 2)


class TestCart(unittest.TestCase):
    """Test Cart shopping cart logic."""

    def setUp(self):
        """Create catalogue and cart for each test."""
        self.catalogue = Catalogue()
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        self.catalogue.add_product("P2", "Bread", 2.50, 10, "bakery")
        self.cart = Cart(self.catalogue)

    def test_cart_starts_empty(self):
        """Test new cart is empty."""
        self.assertTrue(self.cart.is_empty())
        self.assertEqual(self.cart.subtotal(), Decimal("0.00"))

    def test_add_product_to_cart(self):
        """Test adding product to cart."""
        self.cart.add("P1", 2)
        self.assertFalse(self.cart.is_empty())
        items = self.cart.items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].qty, 2)

    def test_add_multiple_products(self):
        """Test adding multiple different products."""
        self.cart.add("P1", 2)
        self.cart.add("P2", 3)
        items = self.cart.items()
        self.assertEqual(len(items), 2)

    def test_add_same_product_twice(self):
        """Test adding same product increases quantity."""
        self.cart.add("P1", 2)
        self.cart.add("P1", 3)
        items = self.cart.items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].qty, 5)

    def test_add_exceeds_stock_fails(self):
        """Test adding more than available stock fails."""
        with self.assertRaises(ValueError):
            self.cart.add("P1", 25)  # Stock is 20

    def test_add_nonexistent_product_fails(self):
        """Test adding non-existent product fails."""
        with self.assertRaises(ValueError):
            self.cart.add("INVALID", 1)

    def test_cart_subtotal_calculation(self):
        """Test cart subtotal calculation."""
        self.cart.add("P1", 2)  # 2 * 3.50 = 7.00
        self.cart.add("P2", 3)  # 3 * 2.50 = 7.50
        # Total: 14.50
        self.assertEqual(self.cart.subtotal(), Decimal("14.50"))

    def test_update_quantity_increase(self):
        """Test increasing item quantity."""
        self.cart.add("P1", 2)
        self.cart.update_qty("P1", 5)
        items = self.cart.items()
        self.assertEqual(items[0].qty, 5)

    def test_update_quantity_decrease(self):
        """Test decreasing item quantity."""
        self.cart.add("P1", 5)
        self.cart.update_qty("P1", 2)
        items = self.cart.items()
        self.assertEqual(items[0].qty, 2)

    def test_update_quantity_to_zero_removes(self):
        """Test updating quantity to 0 removes item."""
        self.cart.add("P1", 2)
        self.cart.update_qty("P1", 0)
        self.assertTrue(self.cart.is_empty())

    def test_update_nonexistent_product_fails(self):
        """Test updating non-existent cart item fails."""
        with self.assertRaises(ValueError):
            self.cart.update_qty("P1", 5)

    def test_remove_item(self):
        """Test removing item from cart."""
        self.cart.add("P1", 2)
        self.cart.add("P2", 3)
        self.cart.remove("P1")
        items = self.cart.items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].product_id, "P2")

    def test_remove_nonexistent_item_fails(self):
        """Test removing non-existent item fails."""
        with self.assertRaises(ValueError):
            self.cart.remove("P1")

    def test_clear_cart(self):
        """Test clearing entire cart."""
        self.cart.add("P1", 2)
        self.cart.add("P2", 3)
        self.cart.clear()
        self.assertTrue(self.cart.is_empty())


# ========== ORDER TESTS ==========

class TestOrderItem(unittest.TestCase):
    """Test OrderItem data holder."""

    def test_orderitem_creation_valid(self):
        """Test creating valid order item."""
        item = OrderItem("P1", "Milk", Decimal("3.50"), 2)
        self.assertEqual(item.product_id, "P1")
        self.assertEqual(item.name, "Milk")
        self.assertEqual(item.unit_price, Decimal("3.50"))
        self.assertEqual(item.qty, 2)

    def test_orderitem_subtotal(self):
        """Test order item subtotal calculation."""
        item = OrderItem("P1", "Milk", Decimal("3.50"), 2)
        self.assertEqual(item.subtotal(), Decimal("7.00"))

    def test_orderitem_to_dict(self):
        """Test order item serialization."""
        item = OrderItem("P1", "Milk", Decimal("3.50"), 2)
        result = item.to_dict()
        self.assertEqual(result["product_id"], "P1")
        self.assertEqual(result["qty"], 2)
        self.assertEqual(result["subtotal"], Decimal("7.00"))


class TestOrder(unittest.TestCase):
    """Test Order entity."""

    def setUp(self):
        """Create order components for tests."""
        self.address = Address("123 Main St", "Melbourne", "VIC", "3000")
        self.items = [
            OrderItem("P1", "Milk", Decimal("3.50"), 2),
            OrderItem("P2", "Bread", Decimal("2.50"), 1)
        ]
        self.shipping = Decimal("7.50")
        self.total = Decimal("16.50")  # (3.50*2 + 2.50*1) + 7.50

    def test_order_creation_valid(self):
        """Test creating valid order."""
        order = Order("ORD123", self.items, self.address, self.shipping, self.total)
        self.assertEqual(order.id, "ORD123")
        self.assertEqual(order.status, "PENDING")
        self.assertEqual(order.total, self.total)

    def test_order_empty_items_fails(self):
        """Test creating order with no items fails."""
        with self.assertRaises(ValueError):
            Order("ORD123", [], self.address, self.shipping, self.total)

    def test_order_negative_total_fails(self):
        """Test creating order with negative total fails."""
        with self.assertRaises(ValueError):
            Order("ORD123", self.items, self.address, self.shipping, Decimal("-10.00"))

    def test_order_calculate_subtotal(self):
        """Test order subtotal calculation."""
        order = Order("ORD123", self.items, self.address, self.shipping, self.total)
        subtotal = order.calculate_subtotal()
        self.assertEqual(subtotal, Decimal("9.00"))  # 7.00 + 2.50

    def test_order_mark_paid_success(self):
        """Test marking order as paid."""
        order = Order("ORD123", self.items, self.address, self.shipping, self.total)
        self.assertIsNone(order.paid_at)

        order.mark_paid()

        self.assertEqual(order.status, "PAID")
        self.assertIsNotNone(order.paid_at)

    def test_order_mark_paid_twice_fails(self):
        """Test marking paid order as paid again fails."""
        order = Order("ORD123", self.items, self.address, self.shipping, self.total)
        order.mark_paid()

        with self.assertRaises(ValueError):
            order.mark_paid()

    def test_order_to_dict(self):
        """Test order serialization."""
        order = Order("ORD123", self.items, self.address, self.shipping, self.total)
        result = order.to_dict()

        self.assertEqual(result["id"], "ORD123")
        self.assertEqual(result["status"], "PENDING")
        self.assertEqual(len(result["items"]), 2)
        self.assertIn("address", result)


# ========== BUSINESS LOGIC TESTS ==========

class TestShippingPolicy(unittest.TestCase):
    """Test ShippingPolicy calculations."""

    def setUp(self):
        """Create catalogue and cart for tests."""
        self.catalogue = Catalogue()
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        self.cart = Cart(self.catalogue)
        self.address = Address("123 Main St", "Melbourne", "VIC", "3000")

    def test_flat_rate_shipping(self):
        """Test flat rate shipping applied."""
        policy = ShippingPolicy(flat_rate=Decimal("7.50"))
        self.cart.add("P1", 2)

        cost = policy.cost_for(self.cart, self.address)

        self.assertEqual(cost, Decimal("7.50"))

    def test_free_shipping_threshold_met(self):
        """Test free shipping when threshold met."""
        policy = ShippingPolicy(flat_rate=Decimal("7.50"), free_over=Decimal("50.00"))
        self.catalogue.add_product("P2", "Expensive Item", 60.00, 10, "luxury")
        self.cart.add("P2", 1)  # Subtotal: 60.00

        cost = policy.cost_for(self.cart, self.address)

        self.assertEqual(cost, Decimal("0.00"))

    def test_free_shipping_threshold_not_met(self):
        """Test flat rate charged when threshold not met."""
        policy = ShippingPolicy(flat_rate=Decimal("7.50"), free_over=Decimal("50.00"))
        self.cart.add("P1", 2)  # Subtotal: 7.00

        cost = policy.cost_for(self.cart, self.address)

        self.assertEqual(cost, Decimal("7.50"))


class TestPaymentService(unittest.TestCase):
    """Test PaymentService."""

    def test_payment_charge_success(self):
        """Test successful payment charge."""
        service = PaymentService()

        success, message = service.charge("ORD123", Decimal("16.50"))

        self.assertTrue(success)
        self.assertIn("approved", message.lower())

    def test_payment_charge_invalid_order_id(self):
        """Test payment with invalid order ID fails."""
        service = PaymentService()

        success, message = service.charge("", Decimal("16.50"))

        self.assertFalse(success)

    def test_payment_charge_negative_amount(self):
        """Test payment with negative amount fails."""
        service = PaymentService()

        success, message = service.charge("ORD123", Decimal("-10.00"))

        self.assertFalse(success)


# ========== INTEGRATION TESTS ==========

class TestCheckoutService(unittest.TestCase):
    """Test CheckoutService orchestration."""

    def setUp(self):
        """Set up complete checkout scenario."""
        self.catalogue = Catalogue()
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        self.catalogue.add_product("P2", "Bread", 2.50, 10, "bakery")

        self.cart = Cart(self.catalogue)
        self.shipping_policy = ShippingPolicy()
        self.payment_service = PaymentService()
        self.checkout_service = CheckoutService(
            self.cart,
            self.shipping_policy,
            self.payment_service
        )
        self.address = Address("123 Main St", "Melbourne", "VIC", "3000")

    def test_checkout_empty_cart_fails(self):
        """Test checkout with empty cart fails."""
        with self.assertRaises(ValueError):
            self.checkout_service.compute_totals(self.address)

    def test_checkout_invalid_address_fails(self):
        """Test checkout with invalid address fails."""
        self.cart.add("P1", 2)
        bad_address = Address("", "Melbourne", "VIC", "3000")

        with self.assertRaises(ValueError):
            self.checkout_service.compute_totals(bad_address)

    def test_checkout_compute_totals(self):
        """Test checkout total calculation."""
        self.cart.add("P1", 2)  # 2 * 3.50 = 7.00
        self.cart.add("P2", 1)  # 1 * 2.50 = 2.50
        # Subtotal: 9.50, Shipping: 7.50, Total: 17.00

        subtotal, shipping, total = self.checkout_service.compute_totals(self.address)

        self.assertEqual(subtotal, Decimal("9.50"))
        self.assertEqual(shipping, Decimal("7.50"))
        self.assertEqual(total, Decimal("17.00"))

    def test_checkout_place_order_success(self):
        """Test successful order placement."""
        self.cart.add("P1", 2)

        order_id, message = self.checkout_service.place_order(self.address)

        self.assertIsNotNone(order_id)
        self.assertIn("approved", message.lower())
        self.assertTrue(self.cart.is_empty())  # Cart cleared

    def test_checkout_place_order_clears_cart(self):
        """Test cart is cleared after successful checkout."""
        self.cart.add("P1", 2)
        self.cart.add("P2", 1)

        self.checkout_service.place_order(self.address)

        self.assertTrue(self.cart.is_empty())


class TestStoreFront(unittest.TestCase):
    """Test StoreFront facade integration."""

    def setUp(self):
        """Set up complete system."""
        self.catalogue = Catalogue()
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        self.catalogue.add_product("P2", "Bread", 2.50, 10, "bakery")
        self.catalogue.add_product("P3", "Cheese", 5.00, 15, "dairy")

        self.cart = Cart(self.catalogue)
        self.shipping_policy = ShippingPolicy()
        self.payment_service = PaymentService()
        self.checkout_service = CheckoutService(
            self.cart,
            self.shipping_policy,
            self.payment_service
        )
        self.storefront = StoreFront(self.catalogue, self.cart, self.checkout_service)

    def test_storefront_browse_products(self):
        """Test browsing all products through storefront."""
        products = self.storefront.browse_products()
        self.assertEqual(len(products), 3)

    def test_storefront_search_products(self):
        """Test product search through storefront."""
        results = self.storefront.search_products("milk")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Milk")

    def test_storefront_filter_by_category(self):
        """Test filtering by category through storefront."""
        results = self.storefront.filter_products_by_category("dairy")
        self.assertEqual(len(results), 2)

    def test_storefront_add_to_cart(self):
        """Test adding to cart through storefront."""
        self.storefront.add_to_cart("P1", 2)
        items, subtotal = self.storefront.view_cart()
        self.assertEqual(len(items), 1)
        self.assertEqual(subtotal, Decimal("7.00"))

    def test_storefront_view_cart(self):
        """Test viewing cart through storefront."""
        self.storefront.add_to_cart("P1", 2)
        self.storefront.add_to_cart("P2", 3)

        items, subtotal = self.storefront.view_cart()

        self.assertEqual(len(items), 2)
        self.assertEqual(subtotal, Decimal("14.50"))

    def test_storefront_update_cart_quantity(self):
        """Test updating cart quantity through storefront."""
        self.storefront.add_to_cart("P1", 2)
        self.storefront.update_cart_quantity("P1", 5)

        items, _ = self.storefront.view_cart()
        self.assertEqual(items[0]["qty"], 5)

    def test_storefront_remove_from_cart(self):
        """Test removing from cart through storefront."""
        self.storefront.add_to_cart("P1", 2)
        self.storefront.add_to_cart("P2", 3)
        self.storefront.remove_from_cart("P1")

        items, _ = self.storefront.view_cart()
        self.assertEqual(len(items), 1)

    def test_storefront_checkout(self):
        """Test complete checkout through storefront."""
        self.storefront.add_to_cart("P1", 2)

        order_id, message = self.storefront.proceed_to_checkout(
            "123 Main St", "Melbourne", "VIC", "3000"
        )

        self.assertIsNotNone(order_id)
        self.assertIn("approved", message.lower())

        # Verify cart is cleared
        items, _ = self.storefront.view_cart()
        self.assertEqual(len(items), 0)


# ========== SCENARIO TESTS ==========

class TestScenarios(unittest.TestCase):
    """Test complete user scenarios end-to-end."""

    def setUp(self):
        """Set up complete system for scenario testing."""
        self.catalogue = Catalogue()
        self.cart = Cart(self.catalogue)
        self.shipping_policy = ShippingPolicy()
        self.payment_service = PaymentService()
        self.checkout_service = CheckoutService(
            self.cart,
            self.shipping_policy,
            self.payment_service
        )
        self.storefront = StoreFront(self.catalogue, self.cart, self.checkout_service)

    def test_scenario_1_admin_creates_products(self):
        """
        Scenario 1: Admin Creates Products (T7)
        1. Empty catalogue
        2. Add product with validation error
        3. Correct and add successfully
        """
        # Step 1: Verify empty
        products = self.catalogue.get_all_products()
        self.assertEqual(len(products), 0)

        # Step 2: Try invalid product (negative price)
        with self.assertRaises(ValueError):
            self.catalogue.add_product("P1", "Milk", -1.00, 20, "dairy")

        # Step 3: Add valid product
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        products = self.catalogue.get_all_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Milk")

    def test_scenario_2_customer_browses_and_shops(self):
        """
        Scenario 2: Customer Browses and Shops (T2 + T3)
        1. Browse all products
        2. Search for "milk"
        3. Filter by category
        4. Add to cart
        5. View cart
        6. Update quantity
        7. Remove item
        8. Add back
        """
        # Setup products
        self.catalogue.add_product("P1", "Whole Milk", 3.50, 20, "dairy")
        self.catalogue.add_product("P2", "Skim Milk", 3.00, 15, "dairy")
        self.catalogue.add_product("P3", "Bread", 2.50, 10, "bakery")

        # Step 1: Browse all
        products = self.storefront.browse_products()
        self.assertEqual(len(products), 3)

        # Step 2: Search
        results = self.storefront.search_products("milk")
        self.assertEqual(len(results), 2)

        # Step 3: Filter
        dairy = self.storefront.filter_products_by_category("dairy")
        self.assertEqual(len(dairy), 2)

        # Step 4: Add to cart
        self.storefront.add_to_cart("P1", 2)

        # Step 5: View cart
        items, subtotal = self.storefront.view_cart()
        self.assertEqual(len(items), 1)
        self.assertEqual(subtotal, Decimal("7.00"))

        # Step 6: Update quantity
        self.storefront.update_cart_quantity("P1", 3)
        items, subtotal = self.storefront.view_cart()
        self.assertEqual(items[0]["qty"], 3)

        # Step 7: Remove
        self.storefront.remove_from_cart("P1")
        items, _ = self.storefront.view_cart()
        self.assertEqual(len(items), 0)

        # Step 8: Add back
        self.storefront.add_to_cart("P1", 1)
        items, _ = self.storefront.view_cart()
        self.assertEqual(len(items), 1)

    def test_scenario_3_customer_checkout(self):
        """
        Scenario 3: Customer Checks Out (T4)
        1. View cart with items
        2. Proceed to checkout
        3. Enter invalid address
        4. Correct address
        5. Confirm order
        6. Verify cart cleared
        """
        # Setup
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")
        self.storefront.add_to_cart("P1", 2)

        # Step 1: View cart
        items, subtotal = self.storefront.view_cart()
        self.assertEqual(len(items), 1)

        # Step 3: Try invalid address (empty street)
        with self.assertRaises(ValueError):
            self.storefront.proceed_to_checkout("", "Melbourne", "VIC", "3000")

        # Step 4 & 5: Valid checkout
        order_id, message = self.storefront.proceed_to_checkout(
            "123 Main St", "Melbourne", "VIC", "3000"
        )
        self.assertIsNotNone(order_id)

        # Step 6: Verify cart cleared
        items, _ = self.storefront.view_cart()
        self.assertEqual(len(items), 0)

    def test_scenario_4_admin_updates_catalogue(self):
        """
        Scenario 4: Admin Updates Catalogue (T7)
        1. View all products
        2. Select product
        3. Edit price
        4. Success
        5. Delete product
        6. Success
        """
        # Setup
        self.catalogue.add_product("P1", "Milk", 3.50, 20, "dairy")

        # Step 1: View
        products = self.catalogue.get_all_products()
        self.assertEqual(len(products), 1)

        # Step 2 & 3: Update price
        self.catalogue.update_product("P1", price=3.75)

        # Step 4: Verify update
        product = self.catalogue.get_product("P1")
        self.assertEqual(product["price"], 3.75)

        # Step 5: Delete
        self.catalogue.delete_product("P1")

        # Step 6: Verify deleted
        products = self.catalogue.get_all_products()
        self.assertEqual(len(products), 0)


# ========== TEST RUNNER ==========

def run_tests():
    """Run all tests and display results."""
    if not IMPORTS_OK:
        print("=" * 70)
        print("IMPORT ERROR: Cannot run tests")
        print("=" * 70)
        return

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestProduct))
    suite.addTests(loader.loadTestsFromTestCase(TestProductType))
    suite.addTests(loader.loadTestsFromTestCase(TestAddress))
    suite.addTests(loader.loadTestsFromTestCase(TestCatalogue))
    suite.addTests(loader.loadTestsFromTestCase(TestCartItem))
    suite.addTests(loader.loadTestsFromTestCase(TestCart))
    suite.addTests(loader.loadTestsFromTestCase(TestOrderItem))
    suite.addTests(loader.loadTestsFromTestCase(TestOrder))
    suite.addTests(loader.loadTestsFromTestCase(TestShippingPolicy))
    suite.addTests(loader.loadTestsFromTestCase(TestPaymentService))
    suite.addTests(loader.loadTestsFromTestCase(TestCheckoutService))
    suite.addTests(loader.loadTestsFromTestCase(TestStoreFront))
    suite.addTests(loader.loadTestsFromTestCase(TestScenarios))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)

    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 70)

    return result


if __name__ == "__main__":
    run_tests()