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

from decimal import Decimal
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


# ========== ADMIN OPERATIONS ==========

def admin_view_products(catalogue: Catalogue) -> None:
    """
    Handle viewing all products (Scenario 1, Step 1 & Scenario 4, Step 1).
    
    Args:
        catalogue: Catalogue instance
        
    TODO:
    - Call catalogue.get_all_products()
    - Display using display_products()
    - Show message if catalogue is empty
    - Pause for user to read
    """
    pass


def admin_add_product(catalogue: Catalogue) -> None:
    """
    Handle adding new product (Scenario 1).
    
    Args:
        catalogue: Catalogue instance
        
    TODO:
    - Print "Add New Product"
    - Prompt for product details:
      - product_id
      - name
      - price (validate positive number - Step 3)
      - stock (validate non-negative integer)
      - type_id (category)
    - If validation fails (e.g., negative price), show error (Step 3) and allow retry (Step 4)
    - Try calling catalogue.add_product(product_id, name, price, stock, type_id)
    - Catch ValueError for validation errors
    - Show success message (Step 5): "Product saved, appears in list"
    - Optionally show updated product list
    - Pause for user to read
    """
    pass


def admin_update_product(catalogue: Catalogue) -> None:
    """
    Handle updating existing product (Scenario 4, Steps 2-4).
    
    Args:
        catalogue: Catalogue instance
        
    TODO:
    - Show all products first (Step 1)
    - Prompt user to select product by ID (Step 2)
    - Verify product exists
    - Prompt for field to update:
      - 1: Name
      - 2: Price (Step 3)
      - 3: Stock
      - 4: Cancel
    - Prompt for new value
    - Validate new value (positive price, non-negative stock)
    - Try calling catalogue.update_product(product_id, **kwargs)
    - Catch ValueError for validation errors
    - Show success message (Step 4): "Product updated"
    - Optionally show updated product details
    - Pause for user to read
    """
    pass


def admin_delete_product(catalogue: Catalogue) -> None:
    """
    Handle deleting product (Scenario 4, Steps 5-6).
    
    Args:
        catalogue: Catalogue instance
        
    TODO:
    - Show all products first
    - Prompt user for product ID to delete (Step 5)
    - Confirm deletion (ask "Are you sure? (y/n)")
    - Try calling catalogue.delete_product(product_id)
    - Catch ValueError if product not found
    - Show success message (Step 6): "Product removed from list"
    - Optionally show updated product list
    - Pause for user to read
    """
    pass


def admin_mode(catalogue: Catalogue) -> None:
    """
    Main loop for admin mode operations.
    
    Args:
        catalogue: Catalogue instance
        
    TODO:
    - Loop until user chooses to go back
    - Clear screen and display admin menu
    - Get user choice
    - Use if/elif to route to appropriate function:
      - 1: admin_view_products()
      - 2: admin_add_product()
      - 3: admin_update_product()
      - 4: admin_delete_product()
      - 5: break (back to main menu)
      - Invalid: show error message
    - Handle any unexpected exceptions gracefully
    """
    pass


# ========== BOOTSTRAP & INITIALIZATION ==========

def bootstrap_system() -> tuple[Catalogue, StoreFront]:
    """
    Initialize all system components (bootstrap process from Assignment 2).
    
    Returns:
        Tuple of (Catalogue, StoreFront) for access in main loop
        
    TODO:
    - Create Catalogue instance
    - Create some sample ProductType instances
    - Create several sample Product instances and add to Catalogue
      - Include products for all scenarios (e.g., "Milk" for demo scenarios)
      - Mix of categories: "Daily Essentials", "Specialty Items"
      - Vary prices and stock levels
    - Create Cart instance (inject Catalogue as dependency)
    - Create ShippingPolicy instance (use default rates)
    - Create PaymentService instance (use default/mock gateway)
    - Create CheckoutService instance (inject Cart, ShippingPolicy, PaymentService)
    - Create StoreFront instance (inject Catalogue, Cart, CheckoutService)
    - Print initialization success message
    - Return (catalogue, storefront) tuple
    """
    pass


def main() -> None:
    """
    Main entry point for the application.
    
    TODO:
    - Call bootstrap_system() to initialize all components
    - Unpack returned (catalogue, storefront) tuple
    - Display banner
    - Enter main loop:
      - Clear screen
      - Display main menu
      - Get user choice
      - Route to appropriate mode:
        - 1: customer_mode(storefront)
        - 2: admin_mode(catalogue)
        - 3: Exit (print goodbye message and break)
        - Invalid: show error message
    - Handle KeyboardInterrupt (Ctrl+C) gracefully with goodbye message
    - Handle any unexpected exceptions with error message
    """
    pass


if __name__ == "__main__":
    """
    Entry point when script is run directly.
    
    TODO:
    - Call main()
    - This allows main.py to be imported without auto-execution (for testing)
    """
    pass
