import sqlite3

def initiate_db():
    connection = sqlite3.connect('db_products.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    )
    ''')
    connection.commit()
    connection.close()

def add_products(title, description, price):
    connection = sqlite3.connect('db_products.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                   (title, description, price))
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('db_products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, title, description, price FROM Products')
    prods = cursor.fetchall()
    connection.close()
    return prods



