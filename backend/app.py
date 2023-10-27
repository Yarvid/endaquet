from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "products.json"

@app.route('/products', methods=['GET'])
def get_products():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            products = json.load(f)
    else:
        products = []
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    product = request.json
    products = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            products = json.load(f)
    products.append(product)
    with open(DATA_FILE, 'w') as f:
        json.dump(products, f)
    return jsonify({"message": "Product added!"}), 201

@app.route('/product/<int:index>', methods=['DELETE'])
def remove_product(index):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            products = json.load(f)
        if 0 <= index < len(products):
            del products[index]
            with open(DATA_FILE, 'w') as f:
                json.dump(products, f)
            return jsonify({"message": "Product removed!"})
    return jsonify({"error": "Invalid index!"}), 400

if __name__ == '__main__':
    app.run(debug=True)
