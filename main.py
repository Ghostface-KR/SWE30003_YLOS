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

from decimal import Decimal, InvalidOperation
from typing import Optional

# Import domain classes
from catalogue import Catalogue, Product, ProductType
from cart import Cart
from checkout_service import CheckoutService
from payment_service import PaymentService
from shipping_policy import ShippingPolicy
from storefront import StoreFront
from address import Address

# Optional: for clearing console
import os


def clear_screen() -> None:
    """
    Clear the console screen for better UX.

    TODO:
    - Detect operating system (os.name)
    - Use 'cls' for Windows, 'clear' for Unix/Mac
    - Call os.system() with appropriate command
    - Handle any errors silently
    """
    pass


def display_banner() -> None:
    """
    Display welcome banner/logo for the application.

    TODO:
    - Print ASCII art or simple text banner
    - Include store name "Your Local Shop"
    - Keep it simple (3-5 lines max)
    """
    pass


def display_main_menu() -> None:
    """
    Display main menu options.

    TODO:
    - Print menu title
    - Print numbered options:
      1. Customer Mode (Browse/Shop/Checkout)
      2. Admin Mode (Manage Products)
      3. Exit
    - Keep formatting clean and readable
    """
    pass


def display_customer_menu() -> None:
    """
    Display customer mode menu options.

    TODO:
    - Print menu title "Customer Menu"
    - Print numbered options:
      1. Browse All Products
      2. Search Products
      3. Filter by Category
      4. View Cart
      5. Add to Cart
      6. Update Cart Quantity
      7. Remove from Cart
      8. Checkout
      9. Back to Main Menu
    - Keep formatting clean
    """
    pass


def display_admin_menu() -> None:
    """
    Display admin mode menu options.

    TODO:
    - Print menu title "Admin Menu"
    - Print numbered options:
      1. View All Products
      2. Add Product
      3. Update Product
      4. Delete Product
      5. Back to Main Menu
    - Keep formatting clean
    """
    pass


def get_user_choice(prompt: str = "Enter choice: ") -> str:
    """
    Get validated user input.

    Args:
        prompt: The prompt message to display

    Returns:
        User's input as string (stripped of whitespace)

    TODO:
    - Display the prompt
    - Get input from user
    - Strip whitespace
    - Return the cleaned input
    - Handle KeyboardInterrupt (Ctrl+C) gracefully
    """
    pass


def display_products(products: list, title: str = "Products") -> None:
    """
    Display a list of products in formatted table.

    Args:
        products: List of product dictionaries
        title: Header title for the list

    TODO:
    - Print title with separator line
    - Check if products list is empty; print "No products found" if so
    - Print table header: "ID | Name | Price | Stock | Category"
    - Print separator line
    - Iterate through products and print each in format:
      "{id} | {name} | ${price} | {stock} units | {type_id}"
    - Print closing separator line
    - Handle missing fields gracefully (use "N/A" for missing data)
    """
    pass


def display_cart_items(items: list, subtotal: Decimal) -> None:
    """
    Display cart contents with subtotal.

    Args:
        items: List of cart item dictionaries
        subtotal: Cart subtotal amount

    TODO:
    - Print title "Shopping Cart"
    - Check if cart is empty; print "Cart is empty" if so
    - Print table header: "Product | Price | Qty | Subtotal"
    - Print separator line
    - Iterate through items and print each in format:
      "{name} | ${unit_price} | {qty} | ${line_subtotal}"
    - Print separator line
    - Print subtotal: "Subtotal: ${subtotal}"
    - Format all prices to 2 decimal places
    """
    pass


def pause() -> None:
    """
    Pause execution until user presses Enter.

    TODO:
    - Print "Press Enter to continue..."
    - Wait for user to press Enter
    - This gives user time to read output before screen clears
    """
    pass


# ========== CUSTOMER OPERATIONS ==========

def customer_browse_all(storefront: StoreFront) -> None:
    """
    Handle browsing all products (Scenario 2, Step 1).

    Args:
        storefront: StoreFront instance

    TODO:
    - Call storefront.browse_products()
    - Display returned products using display_products()
    - Handle empty catalogue case
    - Pause for user to read
    """
    pass


def customer_search(storefront: StoreFront) -> None:
    """
    Handle product search (Scenario 2, Step 2).

    Args:
        storefront: StoreFront instance

    TODO:
    - Prompt user for search keyword
    - Validate input is not empty
    - Call storefront.search_products(query)
    - Display results using display_products()
    - Show message if no results found
    - Pause for user to read
    """
    pass


def customer_filter_by_category(storefront: StoreFront) -> None:
    """
    Handle filtering by category (Scenario 2, Step 3).

    Args:
        storefront: StoreFront instance

    TODO:
    - Display available categories (get from catalogue)
    - Prompt user to enter category name
    - Call storefront.filter_products_by_category(type_id)
    - Display results using display_products()
    - Show message if no results found
    - Pause for user to read
    """
    pass


def customer_view_cart(storefront: StoreFront) -> None:
    """
    Handle viewing cart contents (Scenario 2, Step 5).

    Args:
        storefront: StoreFront instance

    TODO:
    - Call storefront.view_cart()
    - Unpack returned tuple (items, subtotal)
    - Display using display_cart_items()
    - Pause for user to read
    """
    pass


def customer_add_to_cart(storefront: StoreFront) -> None:
    """
    Handle adding product to cart (Scenario 2, Step 4).

    Args:
        storefront: StoreFront instance

    TODO:
    - Prompt user for product ID
    - Prompt user for quantity (default 1)
    - Validate quantity is positive integer
    - Try calling storefront.add_to_cart(product_id, qty)
    - Catch and display ValueError (validation errors like stock, not found)
    - Show success message if added
    - Pause for user to read
    """
    pass


def customer_update_cart(storefront: StoreFront) -> None:
    """
    Handle updating cart item quantity (Scenario 2, Step 6).

    Args:
        storefront: StoreFront instance

    TODO:
    - Show current cart first
    - Prompt user for product ID to update
    - Prompt user for new quantity
    - Validate quantity is non-negative integer
    - Try calling storefront.update_cart_quantity(product_id, qty)
    - Catch and display ValueError (product not in cart, invalid qty)
    - Show success message
    - Pause for user to read
    """
    pass


def customer_remove_from_cart(storefront: StoreFront) -> None:
    """
    Handle removing item from cart (Scenario 2, Step 7).

    Args:
        storefront: StoreFront instance

    TODO:
    - Show current cart first
    - Prompt user for product ID to remove
    - Try calling storefront.remove_from_cart(product_id)
    - Catch and display ValueError (product not in cart)
    - Show success message
    - Pause for user to read
    """
    pass


def customer_checkout(storefront: StoreFront) -> None:
    """
    Handle checkout process (Scenario 3).

    Args:
        storefront: StoreFront instance

    TODO:
    - Show current cart first (Step 1)
    - Check if cart is empty; print error and return if so
    - Print "Proceed to Checkout" (Step 2)
    - Prompt for address fields (Step 3):
      - street (show error if empty - Step 4)
      - city
      - state
      - postcode (validate 4 digits - Step 4)
    - If validation fails, show error and allow retry
    - Once valid address entered (Step 5):
      - Try calling storefront.proceed_to_checkout(street, city, state, postcode)
      - Catch ValueError for address validation errors
      - On success, unpack (order_id, message) tuple
      - Display success message (Step 7): "Payment of ${amount} processed. Order #{order_id} confirmed"
      - Confirm cart is cleared (Step 8)
    - Pause for user to read
    """
    pass


def customer_mode(storefront: StoreFront) -> None:
    """
    Main loop for customer mode operations.

    Args:
        storefront: StoreFront instance

    TODO:
    - Loop until user chooses to go back
    - Clear screen and display customer menu
    - Get user choice
    - Use if/elif to route to appropriate function:
      - 1: customer_browse_all()
      - 2: customer_search()
      - 3: customer_filter_by_category()
      - 4: customer_view_cart()
      - 5: customer_add_to_cart()
      - 6: customer_update_cart()
      - 7: customer_remove_from_cart()
      - 8: customer_checkout()
      - 9: break (back to main menu)
      - Invalid: show error message
    - Handle any unexpected exceptions gracefully
    """
    pass


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

    rows = []
    for product in products:
        rows.append(product.to_dict())

    display_products(rows, "All Products")
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



# ========== BOOTSTRAP & INITIALIZATION ==========

def bootstrap_system() -> tuple[Catalogue, StoreFront]:
    """
    Initialize all system components (bootstrap process from Assignment 2).

    Returns:
        Tuple of (Catalogue, StoreFront) for access in main loop
    """
    catalogue = Catalogue()

    # Register product types with Catalogue
    catalogue.add_type("daily", "Daily Essentials", "Everyday basics and household staples.")
    catalogue.add_type("special", "Specialty Items", "Gourmet and specialty products.")
    catalogue.add_type("produce", "Fresh Produce", "Fruits and vegetables.")
    catalogue.add_type("dairy", "Dairy", "Milk, cheese, yoghurt.")
    catalogue.add_type("bakery", "Bakery", "Bread and pastries.")
    catalogue.add_type("meat", "Meat & Poultry", "Beef, chicken, pork, and more.")
    catalogue.add_type("seafood", "Seafood", "Fresh and frozen seafood.")
    catalogue.add_type("frozen", "Frozen Foods", "Frozen meals, vegetables, desserts.")
    catalogue.add_type("pantry", "Pantry", "Canned goods, sauces, oils, spices, baking.")
    catalogue.add_type("snacks", "Snacks & Confectionery", "Chips, chocolate, lollies.")
    catalogue.add_type("beverages", "Beverages", "Soft drinks, juices, water, coffee, tea.")
    catalogue.add_type("breakfast", "Breakfast & Cereal", "Cereal, oats, spreads.")
    catalogue.add_type("health", "Health & Beauty", "Personal care, toiletries.")
    catalogue.add_type("household", "Household & Cleaning", "Cleaning supplies, paper goods.")
    catalogue.add_type("baby", "Baby", "Nappies, wipes, baby food.")
    catalogue.add_type("pet", "Pet Care", "Pet food and supplies.")

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

    Initialises components, shows the banner, runs the main menu loop, and routes to customer/admin modes. Handles Ctrl+C and unexpected errors gracefully.
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
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
                pause()

    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")
        pause()


if __name__ == "__main__":
    main()
