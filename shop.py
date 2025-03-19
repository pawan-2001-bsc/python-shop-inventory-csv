import csv

try:
    from tabulate import tabulate
    USE_TABULATE = True
except ImportError:
    USE_TABULATE = False

INVENTORY_FILE = "inventory.csv"
SALES_FILE = "sales.csv"

class Product:
    def __init__(self, product_id, name, price, quantity):  # Changed _init_ to __init__
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_list(self):
        return [self.product_id, self.name, self.price, self.quantity]

class Inventory:
    def __init__(self):  # Changed _init_ to __init__
        self.products = {}
        self.load_inventory()

    def load_inventory(self):
        try:
            with open(INVENTORY_FILE, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    if row:  # Skip empty lines
                        product_id, name, price, quantity = row
                        self.products[int(product_id)] = Product(int(product_id), name, float(price), int(quantity))
        except FileNotFoundError:
            with open(INVENTORY_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["product_id", "product_name", "price", "quantity"])

    def save_inventory(self):
        with open(INVENTORY_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["product_id", "product_name", "price", "quantity"])
            for product in self.products.values():
                writer.writerow(product.to_list())

    def add_product(self, product_id, name, price, quantity):
        if product_id in self.products:
            print("Product ID already exists. Try updating the quantity instead.")
            return
        self.products[product_id] = Product(product_id, name, price, quantity)
        self.save_inventory()
        print("Product added successfully!")

    def view_inventory(self):
        if not self.products:
            print("No products in inventory.")
            return
        
        data = [[p.product_id, p.name, p.price, p.quantity] for p in self.products.values()]
        headers = ["ID", "Name", "Price", "Quantity"]

        print("\nInventory List:")
        if USE_TABULATE:
            print(tabulate(data, headers=headers, tablefmt="grid"))
        else:
            print(f"\n{'ID':<5} {'Name':<15} {'Price':<10} {'Quantity':<10}")
            print("-" * 40)
            for row in data:
                print(f"{row[0]:<5} {row[1]:<15} {row[2]:<10} {row[3]:<10}")

class Sale:
    def __init__(self, sale_id):  # Changed _init_ to __init__
        self.sale_id = sale_id
        self.items = []

    def add_item(self, product_id, product_name, quantity_sold, total_price):
        self.items.append([product_id, product_name, quantity_sold, total_price])

    def to_list(self):
        return [[self.sale_id] + item for item in self.items]

class SalesManager:
    def __init__(self):  # Changed _init_ to __init__
        self.sales = []
        self.load_sales()

    def load_sales(self):
        try:
            with open(SALES_FILE, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    if row:  # Skip empty lines
                        self.sales.append(row)
        except FileNotFoundError:
            with open(SALES_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["sale_id", "product_id", "product_name", "quantity_sold", "total_price"])

    def record_sale(self, sale):
        with open(SALES_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            for item in sale.to_list():
                writer.writerow(item)
        self.sales.extend(sale.to_list())

    def view_sales_report(self):
        if not self.sales:
            print("No sales records found.")
            return

        headers = ["Sale ID", "Product ID", "Product Name", "Quantity Sold", "Total Price"]

        print("\nSales Report:")
        if USE_TABULATE:
            print(tabulate(self.sales, headers=headers, tablefmt="grid"))
        else:
            print(f"\n{'Sale ID':<10} {'Product ID':<10} {'Product Name':<15} {'Quantity Sold':<15} {'Total Price':<10}")
            print("-" * 60)
            for row in self.sales:
                print(f"{row[0]:<10} {row[1]:<10} {row[2]:<15} {row[3]:<15} {row[4]:<10}")

class ShopSystem:
    def __init__(self):  # Changed _init_ to __init__
        self.inventory = Inventory()
        self.sales_manager = SalesManager()

    def process_sale(self):
        sale_id = input("Enter Sale ID: ")
        sale = Sale(sale_id)
        sale_made = False

        while True:
            product_id = input("Enter Product ID to sell (or 'done' to finish): ")
            if product_id.lower() == "done":
                break
            if not product_id.isdigit() or int(product_id) not in self.inventory.products:
                print("Invalid Product ID. Try again.")
                continue

            product_id = int(product_id)
            product = self.inventory.products[product_id]
            quantity = input(f"Enter quantity for {product.name}: ")

            if not quantity.isdigit() or int(quantity) <= 0:
                print("Invalid quantity. Try again.")
                continue

            quantity = int(quantity)
            if quantity > product.quantity:
                print("Not enough stock available.")
                continue

            total_price = quantity * product.price
            sale.add_item(product_id, product.name, quantity, total_price)
            product.quantity -= quantity
            sale_made = True

        if sale_made:
            self.inventory.save_inventory()
            self.sales_manager.record_sale(sale)
            print(f"Sale {sale_id} recorded successfully!")
        else:
            print("No items were sold. Sale canceled.")

    def menu(self):
        while True:
            print("\n--- Small Shop Management System ---")
            print("1. View Inventory")
            print("2. Add Product to Inventory")
            print("3. Process a Sale")
            print("4. View Sales Report")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.inventory.view_inventory()
            elif choice == "2":
                try:
                    product_id = int(input("Enter Product ID: "))
                    name = input("Enter Product Name: ")
                    price = float(input("Enter Product Price: "))
                    quantity = int(input("Enter Quantity: "))
                    self.inventory.add_product(product_id, name, price, quantity)
                except ValueError:
                    print("Invalid input. Try again.")
            elif choice == "3":
                self.process_sale()
            elif choice == "4":
                self.sales_manager.view_sales_report()
            elif choice == "5":
                print("Exiting system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":  # Changed _name_ to __name__
    shop = ShopSystem()
    shop.menu()

