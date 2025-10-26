from classes.catalogue import Catalogue
from classes.catalogue import Product
from ui.cli import browseCatalogue

def load_dummy_products(catalogue):
    catalogue.add_product(Product(1, "Milk", "Daily Essentials", 3.50))
    catalogue.add_product(Product(2, "Bread", "Daily Essentials", 2.00))
    catalogue.add_product(Product(3, "Chocolate", "Snacks", 4.80))

if __name__ == "__main__":
    catalogue = Catalogue()
    # cart = Cart()
    load_dummy_products(catalogue)
    browseCatalogue(catalogue)