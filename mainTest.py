from YLOS_system.catalogue.catalogue import Catalogue
from YLOS_system.catalogue.product import Product
from ui.cli import browseCatalogue
from YLOS_system.checkout.cart import Cart

# def load_dummy_products(catalogue):
#     catalogue.add_product(Product(1, "Milk", "Daily Essentials", 3.50))
#     catalogue.add_product(Product(2, "Bread", "Daily Essentials", 2.00))
#     catalogue.add_product(Product(3, "Chocolate", "Snacks", 4.80))

if __name__ == "__mainTest__":
    catalogue = Catalogue()
    # cart = Cart()
    # load_dummy_products(catalogue)
    cart = Cart(catalogue)
    browseCatalogue(catalogue, cart)