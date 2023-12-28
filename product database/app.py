from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database Initialization
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Create Products Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Retrieve all products from the database
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    conn.close()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        # Insert new product into the database
        cursor.execute('INSERT INTO products (name, description, price, quantity) VALUES (?, ?, ?, ?)',
                       (name, description, price, quantity))

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('add_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        # Update product in the database
        cursor.execute('''
            UPDATE products
            SET name=?, description=?, price=?, quantity=?
            WHERE id=?
        ''', (name, description, price, quantity, product_id))

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    # Retrieve product details for editing
    cursor.execute('SELECT * FROM products WHERE id=?', (product_id,))
    product = cursor.fetchone()

    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Delete product from the database
    cursor.execute('DELETE FROM products WHERE id=?', (product_id,))

    conn.commit()
    conn.close()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
