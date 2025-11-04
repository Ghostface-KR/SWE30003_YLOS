#Define the Product class, what it stores 
class Product:
    #Product holds its own id, name, category and price
    def __init__(self, product_id, name, type_id, price, stock):

        self.product_id = product_id
        self.name = name
        self.type_id = type_id
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"[{self.product_id}] {self.name} - ${self.price:.2f}"