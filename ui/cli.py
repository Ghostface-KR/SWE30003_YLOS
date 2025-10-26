from classes.catalogue import Product
from classes.catalogue import Catalogue
# from classes.catalogue import get_available_categories

def show_products(products):
    for p in products:
        print(p)

def browseCatalogue(catalogue):
    while True:
        print("\n1. Browse all products\n2. Search\n3. Filter by category\n4. View cart\n5. Exit")
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

        # elif choice == "4":
        #     items, total = cart.view_cart()
        #     for item in items:
        #         print(f"{item.product.name} x{item.quantity} - ${item.get_subtotal():.2f}")
        #     print(f"Total: ${total:.2f}")

        elif choice == "5":
            break