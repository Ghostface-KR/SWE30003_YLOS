from YLOS_system.catalogue.catalogue import Catalogue
from YLOS_system.catalogue.product import Product

def show_products(products):
    for p in products:
        print(p)

def browseCatalogue(catalogue, cart):
    while True:
        print("\n1. Browse all products"
              "\n2. Search"
              "\n3. Filter by category"
              "\n4. Add product to cart"
              "\n5. View cart"
              "\n6. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            products = catalogue.browse_all()
            show_products(products)

        elif choice == "2":
            keyword = input("Enter a keyword: ")
            results = catalogue.search_by_name(keyword)
            show_products(results)

        elif choice == "3":
            categories = catalogue.get_available_categories()
            if not categories:
                print("No categories available.")
                continue
    
            print("\nAvailable Categories:")
            for idx, cat in enumerate(categories, start=1):
                print(f"{idx}. {cat}")

            try:
                selected = int(input("Select category number: "))
                if selected < 1 or selected > len(categories):
                    print("Invalid category number.")
                    continue
                chosen_category = categories[selected - 1]
                results = catalogue.filter_by_category(chosen_category)
                show_products(results)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            product_id = input("Enter product ID to add: ")
            try:
                qty = int(input("Quantity: "))
                cart.add(product_id, qty)
                print(f"Added {qty} of item {product_id} to cart.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            items = cart.items()
            if not items:
                print("Cart is empty.")
            else:
                print("\nYour cart:")
                for i in items:
                    print(f"{i.name} x{i.qty} @ ${i.unit_price} = ${i.subtotal():.2f}")
                print(f"Subtotal: ${cart.subtotal():.2f}")

        elif choice == "6":
            break