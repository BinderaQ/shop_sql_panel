import sqlite3
conn = sqlite3.connect("shopping.db")
cursor = conn.cursor()

cursor.execute ("""CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL);"""
)

cursor.execute ("""CREATE TABLE IF NOT EXISTS customers (customer_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE);""")
    
cursor.execute ("""CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, order_date DATE NOT NULL, FOREIGN KEY (customer_id) REFERENCES customers(customer_id), FOREIGN KEY (product_id) REFERENCES products(product_id));""")

while True:
    print("1.Додавання продуктів")
    print("2.Додавання клієнтів")
    print("3.Замовлення товарів")
    print("4.Сумарний обсяг продажів")
    print("5.Кількість замовлень на кожного клієнта")
    print("6.Кількість замовлень за весь час")
    print("7.Середній чек замовлення")
    print("8.Найбільш популярна категорія товарів")
    print("9.Загальна кількість придбаних товарів кожної категорії")
    print("10.Оновлення цін")
    print("11.Перегляд усіх продуктів у категорії")
    print("12.Список категорій")
    print("13.Вимкнення")

    shop = input()
    if shop == "1":
        name = input("Введіть назву:")
        category = input("Категорія:")
        price = int(input("Введіть ціну:"))
        cursor.execute("""INSERT INTO products(name,category,price) VALUES (?,?,?)""", (name,category,price))
        print("------------------")
        print(f"Створено {category} {name} з ціною {price}.")
        print("------------------")
        conn.commit()
    elif shop == "2":
        first_name = input("Введіть імя:")
        last_name = input("Введіть фамілію:")
        email = input("Введіть EMAIL:")
        cursor.execute("""INSERT INTO customers(first_name,last_name,email) VALUES (?,?,?)""", (first_name,last_name,email))
        print("------------------")
        print(f"Створено користувача {first_name + ' ' + last_name}. Еmail: {email}.")
        print("------------------")
        conn.commit()
    elif shop == "3":
        customer_id = int(input("Введіть ID покупця:"))
        product_id = int(input("Введіть ID продукта:"))
        quantity = input("Введіть кількість:")
        order_date = input("Введіть дату (Р/М/Д):")
        cursor.execute("""INSERT INTO orders(customer_id,product_id,quantity,order_date) VALUES (?,?,?,?)""", (customer_id,product_id,quantity,order_date))
        print("------------------")
        print(f"{order_date}\nЗамовлено {quantity} продукту з ID {product_id} на покупця з ID {customer_id}.")
        print("------------------")
        conn.commit()
    elif shop == "4":
        cursor.execute("""SELECT SUM(orders.quantity * products.price)
                    AS total_sales
                    FROM orders
                    JOIN products ON orders.product_id = products.product_id""")
        total_sales = cursor.fetchone()[0]
        print("------------------")
        print(f"Обсяг продажів: {total_sales}.")
        print("------------------")
        conn.commit()
    elif shop == "5":
        name = input("Введіть імя клієнта:")
        last_name = input("Введіть фамілію клієнта:")
        cursor.execute("""SELECT COUNT(orders.order_id) AS order_count
                    FROM orders
                    JOIN customers ON orders.customer_id = customers.customer_id
                    WHERE customers.first_name = ? AND customers.last_name = ?""", (name, last_name))
        order_count = cursor.fetchone()[0]
        print("------------------")
        print(f"Кількість замовлень для {name} {last_name}: {order_count}.")
        print("------------------")
    
    elif shop == "6":
        cursor.execute("""SELECT customers.first_name, customers.last_name, COUNT(orders.order_id)
                        FROM customers
                       INNER JOIN orders ON customers.customer_id = orders.customer_id
                        GROUP BY customers.customer_id
                       """)
        results = cursor.fetchall()
        amo = int(0)
        print("------------------")
        for cust in results:
            print(f"Клієнт: {cust[0]} {cust[1]}, Кількість замовлень: {cust[2]}.")
            amo += cust[2]
        print(f"Загальна кількість замовлень: {amo}.") 
        print("------------------")

    elif shop == "7":
        cursor.execute("""SELECT AVG(orders.quantity * products.price) AS average_order_value
                    FROM orders
                    INNER JOIN products ON orders.product_id = products.product_id""")
        average_order_value = cursor.fetchone()[0]
        print("------------------")
        print(f"Середній чек замовлення: {average_order_value}.")
        print("------------------")

    elif shop == "8":
        cursor.execute("""SELECT products.category, COUNT(order_id) AS order_count
                       FROM products
                       JOIN orders ON products.product_id = orders.product_id
                       GROUP BY products.category
                       ORDER BY order_count DESC
                       LIMIT 1""")
        prod_category = cursor.fetchone()
        if prod_category:
            print("------------------")
            print(f"Найбільш популярна категорія товарів: {prod_category[0]} з кількістю замовлень: {prod_category[1]}.")
            print("------------------")
        else:
            print("------------------")
            print("Немає замовлень.")
            print("------------------")

    elif shop == "9":
        cursor.execute("""SELECT products.category, SUM(orders.quantity) AS total_quantity
                       FROM products
                       JOIN orders ON products.product_id = orders.product_id
                       GROUP BY products.category""")
        results = cursor.fetchall()
        if results:
            print("------------------")
            for row in results:
                print(f"Категорія: {row[0]}, Загальна кількість придбаних товарів: {row[1]}.")
            print("------------------")

    elif shop == "10":
        product_id = int(input("Введіть ID продукту для оновлення ціни:"))
        new_price = float(input("Введіть нову ціну:"))
        cursor.execute("""UPDATE products SET price = ? WHERE product_id = ?""", (new_price, product_id))
        print("------------------")
        print(f"Ціна продукту з ID {product_id} оновлена на {new_price}.")
        print("------------------")
        conn.commit()

conn.close()