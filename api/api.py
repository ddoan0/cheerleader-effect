import time
from flask import Flask, request, jsonify
import psycopg2

from config import CONFIG, connection_string

app = Flask(__name__)

con = psycopg2.connect(connection_string)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Skincare list API</h1>"

@app.route('/api/products', methods=['GET'])
def get_products():
    """Query all products in the db"""
    cur = con.cursor()
    cur.execute("SELECT * FROM products")
    items = cur.fetchall()
    con.commit()
    cur.close()
    return jsonify(items)

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product_by_id(id):
    """Query product with a specific id"""
    cur = con.cursor()
    cur.execute(f"SELECT * FROM products WHERE id = {id}")
    items = cur.fetchall()
    con.commit()
    cur.close()
    return jsonify(items)

@app.route('/api/products/create', methods=['POST'])
def create_product():
    name = request.form.get('name')
    description = request.form.get('description')
    brand = request.form.get('brand')
    
    cur = con.cursor()
    cur.execute(f"INSERT INTO products (name, description, brand) VALUES (%s, %s, %s)", (name, description, brand))
    con.commit()
    cur.close()
    return "Product Added"

@app.route('/api/products/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    cur = con.cursor()
    cur.execute(f"DELETE FROM products WHERE id = {id}")
    con.commit()
    cur.close()
    return "Product Deleted"

"""Get a list and display its products"""
# TODO: May need to get id parameter through <int: x>
@app.route('/api/lists/<int:list_id>', methods=['GET'])
def get_list(list_id):
    # Use list_id to query db for list
    # return list of products
    cur = con.cursor()
    cur.execute(f"WITH ids AS (SELECT UNNEST(productids) FROM lists WHERE id = {list_id}) SELECT * FROM products WHERE id IN (SELECT * FROM ids)")
    items = cur.fetchall()
    con.commit()
    cur.close()
    return jsonify(items)
# TODO: Create, Update, Delete a Product List
