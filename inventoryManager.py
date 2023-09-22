#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install mysql


# In[2]:


import mysql.connector
from mysql.connector import errorcode

class InventoryManager:
    def __init__(self, host, user, password, database):
        self.db_connection = None
        try:
            self.db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.db_connection.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Access denied. Check your credentials.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: Database does not exist.")
            else:
                print(f"Error: {err}")

    def __del__(self):
        if self.db_connection:
            self.db_connection.close()

    def add_product(self, product_name, quantity):
        try:
            sql = "INSERT INTO Inventory (ProductName, Quantity, LastUpdated) VALUES (%s, %s, NOW())"
            values = (product_name, quantity)
            self.cursor.execute(sql, values)
            self.db_connection.commit()
            print(f"Added {quantity} units of {product_name} to inventory.")
        except mysql.connector.Error as err:
            print(f"Error adding product: {err}")

    def remove_product(self, product_name):
        try:
            sql = "DELETE FROM Inventory WHERE ProductName = %s"
            values = (product_name,)
            self.cursor.execute(sql, values)
            self.db_connection.commit()
            print(f"Removed {product_name} from inventory.")
        except mysql.connector.Error as err:
            print(f"Error removing product: {err}")

    def update_quantity(self, product_name, quantity):
        try:
            sql = "UPDATE Inventory SET Quantity = %s, LastUpdated = NOW() WHERE ProductName = %s"
            values = (quantity, product_name)
            self.cursor.execute(sql, values)
            self.db_connection.commit()
            print(f"Updated quantity of {product_name} to {quantity}.")
        except mysql.connector.Error as err:
            print(f"Error updating quantity: {err}")

    def check_stock_level(self, product_name):
        try:
            sql = "SELECT Quantity FROM Inventory WHERE ProductName = %s"
            values = (product_name,)
            self.cursor.execute(sql, values)
            row = self.cursor.fetchone()
            if row:
                return row[0]
            else:
                return 0
        except mysql.connector.Error as err:
            print(f"Error checking stock level: {err}")
            return 0

# Sample usage of the inventory manager

host = "localhost"
user = "inventory_user"
password = "pass123"
database = "Inventory"

inventory_manager = InventoryManager(host, user, password, database)

# Adding products to the inventory
for i in range(1, 101):
    product_name = f"Product {i}"
    quantity = 10 + i  # Just an example for varying quantities
    inventory_manager.add_product(product_name, quantity)

# Updating quantity of a product
product_name = "Product 1"
new_quantity = 50
inventory_manager.update_quantity(product_name, new_quantity)

# Removing a product from the inventory
product_name = "Product 2"
inventory_manager.remove_product(product_name)

# Checking stock level
product_name = "Product 3"
stock_level = inventory_manager.check_stock_level(product_name)
print(f"Stock level of {product_name}: {stock_level}")


# In[ ]:




