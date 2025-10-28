class Product:
    def __init__(self, product_id, name, category, price):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price

    def __str__(self):
        return f"[{self.product_id}] {self.name} - ${self.price:.2f}"


class Catalogue:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def browse_all(self):
        return self.products

    def search_by_name(self, keyword):
        return [p for p in self.products if keyword.lower() in p.name.lower()]

    def filter_by_category(self, category):
        return [p for p in self.products if p.category.lower() == category.lower()]

    def get_available_categories(self):
        return sorted(set(p.category for p in self.products))