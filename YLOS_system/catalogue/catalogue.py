from YLOS_system.catalogue.product import Product
import json 
from pathlib import Path

class Catalogue:
    def __init__(self, data_file="data/products.json"):
        self.data_file = Path(data_file)
        self.products = []
        self.load_from_file()

    #Save products to a file (acting as a database)

    def load_from_file(self):
        if not self.data_file.exists():
            print("No product data file found")
            self.products = []
            return
        
        with open(self.data_file, "r") as f:
            data = json.load(f)
            self.products = [Product(**p) for p in data]
    
    def save_to_file(self):
        #Save all products to JSON file.
        with open(self.data_file, "w") as f:
            json.dump([p.__dict__ for p in self.products], f, indent=2)    
    
    #Core Catalogue functions 
    def browse_all(self):
        return self.products

    def add_product(self, product):
        self.products.append(product)
        self.save_to_file()

    def delete_product(self, product_id):
        self.products = [p for p in self.products if str(p.product_id) != str(product_id)]
        self.save_to_file()

    def modify_product(self, product_id, name=None, category=None, price=None, stock=None):
        for p in self.products:
            if str(p.product_id) == str(product_id):
                if name is not None:
                    p.name = name
                if category is not None:
                    p.category = category
                if price is not None:
                    p.price = price
                if stock is not None:
                    p.stock = stock
                self.save_to_file()
                return
        raise ValueError("Product not found")

    def search_by_name(self, keyword):
        return [p for p in self.products if keyword.lower() in p.name.lower()]

    def filter_by_category(self, category):
        return [p for p in self.products if p.category.lower() == category.lower()]

    def get_available_categories(self):
        return sorted(set(p.category for p in self.products))
    
    def get_product(self, product_id):
        for p in self.products:
            if str(p.product_id) == str(product_id):
                return {
                    "id": p.product_id,
                    "name": p.name,
                    "price": float(p.price),
                    "stock": getattr(p, "stock", 0)
                }
        return None