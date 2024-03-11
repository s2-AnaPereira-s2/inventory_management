
import os
import sqlite3

warehouses = ["warehouse1", "warehouse2"]

os.chdir(os.path.dirname(__file__))

def check_for_product(product_name):
    """Checks if product exists in inventory"""
    try:
        with sqlite3.connect('inventory.db') as conn:
            curs = conn.cursor()
            curs.execute("""
                    SELECT name FROM inventory
                    WHERE name=?
                    """, (product_name,))        
            product_info = curs.fetchone()
            if product_info:
                return True
            else:
                return False
    except sqlite3.Error as err:
        print("An unexpected error occurred: ", err)
        return False

def delete_func(product_name):
    """Delete a product from the inventory"""
    product_exists = check_for_product(product_name)
    if product_exists:
        try:
            with sqlite3.connect('inventory.db') as conn:
                delete = conn.cursor()
                delete.execute('DELETE FROM inventory WHERE name=?', (product_name,))
                return True
        except sqlite3.Error as err:
            return ("An error has occurred: ", err)
    else:
        return False

def add_new_product(product_name, quantity, price, location):
    product_exists = check_for_product(product_name)
    if product_exists:
        return False   
    try:
        with sqlite3.connect("inventory.db") as conn:
            curs = conn.cursor()
            curs.execute("""
                         INSERT INTO inventory (name, quantity, price, location)
                         VALUES (?, ?, ?, ?)
                        """, (product_name, quantity, price, location))
            return True
    except sqlite3.Error:
        return False


def update_product(product_name, new_quantity, new_price, new_location):
    product_exists = check_for_product(product_name)
    if product_exists:
        try:
            with sqlite3.connect("inventory.db") as conn:
                curs = conn.cursor()
                curs.execute("""
                        SELECT * FROM inventory
                        WHERE name=?
                        """, (product_name,))
                product_info = curs.fetchone()
                price = product_info[3]
                location = product_info[4]
                quantity = product_info[2]
                
                if new_price:
                    price = new_price
                if new_location:
                    location = new_location
                if new_quantity:
                    quantity = new_quantity

                curs.execute("""
                            UPDATE inventory
                            SET quantity=?, price=?, location=?
                            WHERE name=?
                            """, (quantity, price, location, product_name))             
                return True
        except sqlite3.Error as err:
            return ("Error: ", err)
    else:
        return False
    


def display_products():
    """Displays all the product names in inventory"""
    products_available = []
    try:
        with sqlite3.connect('inventory.db') as conn:
            products = conn.cursor()
            products.execute('SELECT * FROM inventory')
            total_products = products.fetchall()
            
            for product in total_products:
                products_available.append(f"ID- {product[0]} | Product name- {product[1]} | Quantity- {product[2]} | Price- {product[3]} | Location- {product[4]}")
        return products_available
    except sqlite3.Error as err:
        return ("An error has occured", err)
    

