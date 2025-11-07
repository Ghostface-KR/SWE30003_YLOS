import os
from decimal import Decimal, InvalidOperation
from typing import Optional, Tuple
from .catalogue.catalogue import Catalogue
from .catalogue.product import Product
from .checkout.cart import Cart
from .checkout.checkout_service import CheckoutService
from .checkout.payment_service import PaymentService
from .checkout.shipping_policy import ShippingPolicy
from .storefront.storefront import StoreFront
from .checkout.address import Address

"""
main.py - Entry point for YLOS (Your Local Shop Online Store) System
Provides command-line textual interface for all scenarios.

Covers 4 business areas:
- T2: Browse/Search Catalogue
- T3: Manage Shopping Cart
- T4: Checkout & Payment
- T7: Maintain Product Catalogue (Admin)

Scenarios demonstrated:
1. Admin Creates Products (T7)
2. Customer Browses and Shops (T2 + T3)
3. Customer Checks Out (T4)
4. Admin Updates Catalogue (T7)
"""

def clear_screen() -> None:
    """Clear the console screen for better UX."""
    try:
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Mac
            os.system('clear')
    except:
        pass  # Silently handle any errors


def display_banner() -> None:
    """Display welcome banner/logo for the application."""
    print("\n" + "="*50)
    print("    YOUR LOCAL SHOP - Online Store")
    print("    Quality Products at Your Fingertips")
    print("="*50 + "\n")


def exit_program() -> None:
    """Handle program exit gracefully."""
    print("\n" + "="*50)
    print("  Thank you for shopping at Your Local Shop!")
    print("  We look forward to serving you again soon.")
    print("="*50 + "\n")


def display_main_menu() -> None:
    """Display main menu options."""
    print("\n===== MAIN MENU =====")
    print("1. Customer Mode (Browse/Shop/Checkout)")
    print("2. Admin Mode (Manage Products)")
    print("3. Exit")
    print("="*21)


def display_customer_menu() -> None:
    """Display customer mode menu options."""
    print("\n===== CUSTOMER MENU =====")
    print("1. Browse All Products")
    print("2. Search Products")
    print("3. Filter by Category")
    print("4. View Cart")
    print("5. Add to Cart")
    print("6. Update Cart Quantity")
    print("7. Remove from Cart")
    print("8. Checkout")
    print("9. Back to Main Menu")
    print("="*25)


def display_admin_menu() -> None:
    """Display admin mode menu options."""
    print("\n===== ADMIN MENU =====")
    print("1. View All Products")
    print("2. Add Product")
    print("3. Update Product")
    print("4. Delete Product")
    print("5. Back to Main Menu")
    print("="*22)


def get_user_choice(prompt: str = "Enter choice: ") -> str:
    """Get validated user input."""
    try:
        user_input = input(prompt)
        return user_input.strip()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return ""


def display_products(products: list, title: str = "Products") -> None:
    """Display a list of products in formatted table."""
    print(f"\n===== {title} =====")
    print("-" * 70)

    if not products:
        print("No products found.")
        print("-" * 70)
        return

    print(f"{'ID':<5} | {'Name':<25} | {'Price':<10} | {'Stock':<10} | {'Category':<10}")
    print("-" * 70)

    for product in products:
        product_id = product.get('id', 'N/A')
        name = product.get('name', 'N/A')
        price = product.get('price', 0)
        stock = product.get('stock', 0)
        type_id = product.get('type_id', 'N/A')

        print(f"{product_id:<5} | {name:<25} | ${price:<9.2f} | {stock:<10} units | {type_id:<10}")

    print("-" * 70)


def display_cart_items(items: list, subtotal: Decimal) -> None:
    """Display cart contents with subtotal."""
    print("\n===== Shopping Cart =====")
    print("-" * 70)

    if not items:
        print("Cart is empty.")
        print("-" * 70)
        return

    print(f"{'ID':<5} | {'Product':<25} | {'Price':<10} | {'Qty':<5} | {'Subtotal':<10}")
    print("-" * 70)

    for item in items:
        product_id = item.get('product_id', 'N/A')
        name = item.get('name', 'N/A')
        unit_price = item.get('unit_price', Decimal('0'))
        qty = item.get('qty', 0)
        line_subtotal = item.get('subtotal', Decimal('0'))

        print(f"{product_id:<5} | {name:<25} | ${unit_price:<9.2f} | {qty:<5} | ${line_subtotal:<9.2f}")


    print("-" * 70)
    print(f"{'Subtotal:':<49} ${subtotal:.2f}")
    print("-" * 70)


def pause() -> None:
    """Pause execution until user presses Enter."""
    input("\nPress Enter to continue...")


# ========== CUSTOMER OPERATIONS ==========

def customer_browse_all(storefront: StoreFront) -> None:
    """Handle browsing all products (Scenario 2, Step 1)."""
    products = storefront.browse_products()
    display_products(products, "All Products")
    pause()


def customer_search(storefront: StoreFront) -> None:
    """Handle product search (Scenario 2, Step 2)."""
    query = get_user_choice("Enter search keyword: ")

    if not query:
        print("Search keyword cannot be empty.")
        pause()
        return

    products = storefront.search_products(query)

    if not products:
        print(f"No products found matching '{query}'.")
    else:
        display_products(products, f"Search Results for '{query}'")

    pause()


def customer_filter_by_category(storefront: StoreFront) -> None:
    """Handle filtering by category (Scenario 2, Step 3)."""
    print("\nAvailable Categories:")
    print("- Daily Essentials")
    print("- Fruit")
    print("- Vegetables")
    print("- Snacks")
    print("- Pantry")
    print("- Beverages")

    category = get_user_choice("\nEnter category name: ")

    if not category:
        print("Category name cannot be empty.")
        pause()
        return

    products = storefront.filter_products_by_category(category)

    if not products:
        print(f"No products found in category '{category}'.")
    else:
        display_products(products, f"Products in '{category}' Category")

    pause()


def customer_view_cart(storefront: StoreFront) -> None:
    """Handle viewing cart contents (Scenario 2, Step 5)."""
    items, subtotal = storefront.view_cart()
    display_cart_items(items, subtotal)
    pause()


def customer_add_to_cart(storefront: StoreFront) -> None:
    """Handle adding product to cart (Scenario 2, Step 4)."""

    # Step 1: Show all available products
    products = storefront.browse_products()
    display_products(products, "Available Products to Add")
    
    if not products:
        print("No products available to add.")
        pause()
        return

    # Step 2: Ask user which product to add
    product_id = get_user_choice("Enter product ID to add: ")

    if not product_id:
        print("Product ID cannot be empty.")
        pause()
        return

    # Step 3: Ask quantity
    qty_str = get_user_choice("Enter quantity (default 1): ")
    qty = 1

    if qty_str:
        try:
            qty = int(qty_str)
            if qty <= 0:
                print("Quantity must be a positive integer.")
                pause()
                return
        except ValueError:
            print("Invalid quantity. Please enter a valid number.")
            pause()
            return

    # Step 4: Try to add to cart
    try:
        storefront.add_to_cart(product_id, qty)
        print(f"✅ Successfully added {qty} unit(s) of product ID {product_id} to cart.")
    except ValueError as e:
        print(f"⚠️ Error: {e}")

    pause()


def customer_update_cart(storefront: StoreFront) -> None:
    """Handle updating cart item quantity (Scenario 2, Step 6)."""
    items, subtotal = storefront.view_cart()
    display_cart_items(items, subtotal)

    if not items:
        pause()
        return

    product_id = get_user_choice("\nEnter product ID to update: ")

    if not product_id:
        print("Product ID cannot be empty.")
        pause()
        return

    qty_str = get_user_choice("Enter new quantity: ")

    try:
        qty = int(qty_str)
        if qty < 0:
            print("Quantity must be a non-negative integer.")
            pause()
            return
    except ValueError:
        print("Invalid quantity. Please enter a valid number.")
        pause()
        return

    try:
        storefront.update_cart_quantity(product_id, qty)
        print(f"Successfully updated quantity for product {product_id} to {qty}.")
    except ValueError as e:
        print(f"Error: {e}")

    pause()


def customer_remove_from_cart(storefront: StoreFront) -> None:
    """Handle removing a specified quantity from cart (Scenario 2, Step 7)."""
    items, subtotal = storefront.view_cart()
    display_cart_items(items, subtotal)

    if not items:
        pause()
        return

    product_id = get_user_choice("\nEnter product ID to remove from cart: ")

    if not product_id:
        print("Product ID cannot be empty.")
        pause()
        return

    # Find the product in cart
    product_in_cart = next((item for item in items if item['product_id'] == product_id), None)

    if not product_in_cart:
        print("Product not found in cart.")
        pause()
        return

    current_qty = product_in_cart['qty']
    qty_str = get_user_choice(f"Enter quantity to remove (1-{current_qty}, default {current_qty}): ")

    if not qty_str:
        qty_to_remove = current_qty  # default to removing all
    else:
        try:
            qty_to_remove = int(qty_str)
            if qty_to_remove <= 0:
                print("Quantity must be positive.")
                pause()
                return
            if qty_to_remove > current_qty:
                print(f"You cannot remove more than {current_qty} units.")
                pause()
                return
        except ValueError:
            print("Invalid quantity. Please enter a valid number.")
            pause()
            return

    try:
        new_qty = current_qty - qty_to_remove
        if new_qty <= 0:
            storefront.remove_from_cart(product_id)
            print(f"Removed all units of product {product_id} from cart.")
        else:
            storefront.update_cart_quantity(product_id, new_qty)
            print(f"Removed {qty_to_remove} unit(s) of product {product_id}. New quantity: {new_qty}")
    except ValueError as e:
        print(f"Error: {e}")

    pause()


def customer_checkout(storefront: StoreFront) -> None:
    """Handle checkout process (Scenario 3)."""
    # Step 1: Show current cart
    items, subtotal = storefront.view_cart()
    display_cart_items(items, subtotal)

    if not items:
        print("Cannot checkout with an empty cart.")
        pause()
        return

    # Step 2: Proceed to Checkout
    print("\n===== Proceed to Checkout =====")

    # Step 3 & 4: Prompt for address fields with validation
    while True:
        street = get_user_choice("Enter street address: ")
        if not street:
            print("Error: Street address cannot be empty.")
            continue

        city = get_user_choice("Enter city: ")
        state = get_user_choice("Enter state: ")
        postcode = get_user_choice("Enter postcode (4 digits): ")

        # Validate postcode (4 digits)
        if not postcode.isdigit() or len(postcode) != 4:
            print("Error: Postcode must be exactly 4 digits.")
            retry = get_user_choice("Try again? (y/n): ")
            if retry.lower() != 'y':
                print("Checkout cancelled.")
                pause()
                return
            continue

        # Step 5: Address entered successfully
        try:
            # Step 6 & 7: Process checkout
            order_id, message = storefront.proceed_to_checkout(street, city, state, postcode)
            print(f"\n{message}")
            print(f"Order #{order_id} confirmed.")

            # Step 8: Verify cart is cleared
            items, subtotal = storefront.view_cart()
            if not items:
                print("Cart has been cleared.")

            break
        except ValueError as e:
            print(f"Error: {e}")
            retry = get_user_choice("Try again? (y/n): ")
            if retry.lower() != 'y':
                print("Checkout cancelled.")
                break

    pause()


def customer_mode(storefront: StoreFront) -> None:
    """Main loop for customer mode operations."""
    while True:
        try:
            clear_screen()
            display_banner()
            display_customer_menu()

            choice = get_user_choice()

            if choice == '1':
                customer_browse_all(storefront)
            elif choice == '2':
                customer_search(storefront)
            elif choice == '3':
                customer_filter_by_category(storefront)
            elif choice == '4':
                customer_view_cart(storefront)
            elif choice == '5':
                customer_add_to_cart(storefront)
            elif choice == '6':
                customer_update_cart(storefront)
            elif choice == '7':
                customer_remove_from_cart(storefront)
            elif choice == '8':
                customer_checkout(storefront)
            elif choice == '9':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 9.")
                pause()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            pause()


# ========== Kale's Sections Below ==========


# ========== ADMIN OPERATIONS ==========

def admin_view_products(catalogue: Catalogue) -> None:
    """
    Handle viewing all products (Scenario 1, Step 1 & Scenario 4, Step 1).

    Args:
        catalogue: Catalogue instance
    """
    products = catalogue.get_all_products()

    if len(products) == 0:
        print("Catalogue is empty")
        pause()
        return

    display_products(products, "All Products")
    pause()

def admin_add_product(catalogue: Catalogue) -> None:
    """
    Handle adding new product (Scenario 1).

    Args:
        catalogue: Catalogue instance
    """
    print("Add New Product")
    product_id = input("Product ID: ")
    name = input("Product name: ")
    price = input("Product price: ")
    stock = input("Product stock: ")
    type_id = input("Product type: ")

    product_id = product_id.strip()
    name = name.strip()
    price = price.strip()
    stock = stock.strip()
    type_id = type_id.strip()

    if not all ([product_id, name, type_id]):
        print("Product ID and name and type are required")
        pause()
        return

    try:
        price_amount = Decimal(price)
        stock_qty = int(stock)
        if price_amount <= 0:
            print("Price must be positive")
            pause()
            return
        if stock_qty < 0:
            print("Stock cannot be negative")
            pause()
            return
        catalogue.add_product(product_id, name, price_amount, stock_qty, type_id)
        print(f"{name} saved, appears in list")
        admin_view_products(catalogue)
        return
    except ValueError as e:
        print(f"Error: {e}")
        pause()
        return
    except InvalidOperation:
        print("Price must be a valid number")
        pause()
        return


def admin_update_product(catalogue: Catalogue) -> None:
    """
    Handle updating existing product (Scenario 4, Steps 2-4).

    Args:
        catalogue: Catalogue instance
    """
    admin_view_products(catalogue)
    product_id_to_update = input("Product ID: ")
    product_id = product_id_to_update.strip()

    selected_product = catalogue.get_product(product_id)

    if selected_product is None:
        print("Product not found")
        pause()
        return

    print("What would you like to update?\n1. Name\n2. Price\n3. Stock\n4. Cancel")

    choice = input("Enter choice (1-4): ").strip()

    if choice == "4":
        print("Update cancelled.")
        pause()
        return

    elif choice == "1":
        new_name = input("New name: ").strip()
        if not new_name:
            print("Name cannot be empty.")
            pause()
            return
        try:
            catalogue.update_product(product_id, name=new_name)
            print("Product updated.")
            admin_view_products(catalogue)
            return
        except ValueError as e:
            print(f"Error: {e}")
            pause()
            return

    elif choice == "2":
        new_price_str = input("New price: ").strip()
        try:
            new_price = Decimal(new_price_str)
            if new_price <= 0:
                print("Price must be positive.")
                pause()
                return
            catalogue.update_product(product_id, price=new_price)
            print("Product updated.")
            admin_view_products(catalogue)
            return
        except InvalidOperation:
            print("Price must be a valid number.")
            pause()
            return
        except ValueError as e:
            print(f"Error: {e}")
            pause()
            return

    elif choice == "3":
        new_stock_str = input("New stock: ").strip()
        try:
            new_stock = int(new_stock_str)
            if new_stock < 0:
                print("Stock cannot be negative.")
                pause()
                return
            catalogue.update_product(product_id, stock=new_stock)
            print("Product updated.")
            admin_view_products(catalogue)
            return
        except ValueError as e:
            print(f"Error: {e}")
            pause()
            return

    else:
        print("Invalid choice.")
        pause()
        return


def admin_delete_product(catalogue: Catalogue) -> None:
    """
    Handle deleting product (Scenario 4, Steps 5-6).

    Args:
        catalogue: Catalogue instance
    """
    admin_view_products(catalogue)
    product_id_to_delete = input("Product ID: ")
    product_id = product_id_to_delete.strip()
    confirm_deletion = input("Are you sure? (y/n) ").strip().lower()

    if confirm_deletion == "y":
        try:
            catalogue.delete_product(product_id)
            print("Product deleted.")
            admin_view_products(catalogue)
            return
        except ValueError as e:
            print(f"Error: {e}")
            pause()
            return
    else:
        print("Product deletion cancelled.")
        pause()
        return

def admin_mode(catalogue: Catalogue) -> None:
    """
    Main loop for admin mode operations.

    Args:
        catalogue: Catalogue instance
    """
    while True:
        try:
            clear_screen()
            display_admin_menu()
            choice = input("Enter choice (1-5): ").strip()
            if choice == "1":
                admin_view_products(catalogue)
            elif choice == "2":
                admin_add_product(catalogue)
            elif choice == "3":
                admin_update_product(catalogue)
            elif choice == "4":
                admin_delete_product(catalogue)
            elif choice == "5":
                break
            else:
                print("Invalid choice.")
                pause()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            pause()



# ========== BOOTSTRAP & INITIALIZATION ==========

def bootstrap_system() -> Tuple[Catalogue, StoreFront]:
    """
    Initialize all system components (bootstrap process from Assignment 2).

    Returns:
        Tuple of (Catalogue, StoreFront) for access in main loop
    """
    catalogue = Catalogue()

    cart = Cart(catalogue)
    shipping_policy = ShippingPolicy()
    payment_service = PaymentService()
    checkout_service = CheckoutService(cart, shipping_policy, payment_service)
    storefront = StoreFront(catalogue, cart, checkout_service)

    print("Bootstrap Initialised")

    return catalogue, storefront


def main() -> None:
    """
    Main entry point for the application.

    Initialises components, shows the banner, runs the main menu loop, and routes to customer/admin modes. 
    Handles Ctrl+C and unexpected errors gracefully.
    """
    try:
        # Initialize core components
        catalogue, storefront = bootstrap_system()

        # Show banner once
        display_banner()

        # Main application loop
        while True:
            clear_screen()
            display_main_menu()
            choice = input("Enter choice (1-3): ").strip()

            if choice == "1":
                customer_mode(storefront)
            elif choice == "2":
                admin_mode(catalogue)
            elif choice == "3":
                exit_program()
                break
            else:
                print("Invalid choice.")
                pause()

    except KeyboardInterrupt:
        exit_program()
    except Exception as e:
        print(f"Error: {e}")
        pause()


if __name__ == "__main__":
    main()

# python3 -m YLOS_system.main