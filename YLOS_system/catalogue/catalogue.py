from .product import Product
from typing import List, Optional, Dict, Any
import json
from pathlib import Path
from decimal import Decimal


class Catalogue:
    def __init__(self, data_file="data/products.json"):
        self.data_file = Path(data_file)
        self.products = []  # List of Product objects
        self.load_from_file()

    def load_from_file(self):
        if not self.data_file.exists():
            self.products = []
            return

        with open(self.data_file, "r") as f:
            data = json.load(f)
            self.products = [Product(
                product_id=item["product_id"],
                name=item["name"],
                category=item.get("category", ""),
                price=item["price"],
                stock=item["stock"]
            ) for item in data]

    def save_to_file(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w") as f:
            products_list = [{
                "product_id": p.product_id,
                "name": p.name,
                "price": p.price,
                "stock": p.stock,
                "category": p.category
            } for p in self.products]
            json.dump(products_list, f, indent=2)

    def get_all_products(self) -> List[Dict[str, Any]]:
        return [{
            "product_id": p.product_id,
            "id": p.product_id,     # alias used by UI tables
            "name": p.name,
            "price": Decimal(str(p.price)),
            "stock": p.stock,
            "category": p.category
        } for p in self.products]

    def add_product(self, product_id: str, name: str, price: float,
                    stock: int, category: str) -> None:
        # Validation
        if any(p.product_id == product_id for p in self.products):
            raise ValueError(f"Product '{product_id}' already exists")

        product = Product(product_id, name, category, price, stock)
        self.products.append(product)
        self.save_to_file()

    def delete_product(self, product_id: str) -> None:
        original_length = len(self.products)
        self.products = [p for p in self.products if p.product_id != product_id]
        if len(self.products) == original_length:
            raise ValueError(f"Product '{product_id}' not found")
        self.save_to_file()

    def update_product(self, product_id: str, name: Optional[str] = None,
                       price: Optional[float] = None, stock: Optional[int] = None) -> None:
        for p in self.products:
            if p.product_id == product_id:
                if name is not None:
                    p.name = name
                if price is not None:
                    p.price = price
                if stock is not None:
                    p.stock = stock
                self.save_to_file()
                return
        raise ValueError(f"Product '{product_id}' not found")

    def search_products(self, query: str) -> List[Dict[str, Any]]:
        if not isinstance(query, str):
            raise ValueError("query must be a string")
        keyword = query.strip().lower()
        if keyword == "":
            return self.get_all_products()

        matches = [p for p in self.products if keyword in p.name.lower()]
        return [{
            "product_id": p.product_id,
            "id": p.product_id,
            "name": p.name,
            "price": Decimal(str(p.price)),
            "stock": p.stock,
            "category": p.category
        } for p in matches]

    def filter_by_type(self, type_id: str) -> List[Dict[str, Any]]:
        if not type_id:
            raise ValueError("type_id must be non-empty")

        keyword = type_id.strip().lower()
        matches = [p for p in self.products if p.category and p.category.lower() == keyword]
        return [{
            "product_id": p.product_id,
            "id": p.product_id,
            "name": p.name,
            "price": Decimal(str(p.price)),
            "stock": p.stock,
            "category": p.category
        } for p in matches]

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        if not product_id:
            raise ValueError("product_id must be non-empty")

        for p in self.products:
            if p.product_id == product_id:
                return {
                    "product_id": p.product_id,
                    "id": p.product_id,
                    "name": p.name,
                    "price": Decimal(str(p.price)),
                    "stock": p.stock,
                    "category": p.category
                }
        return None
