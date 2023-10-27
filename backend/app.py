from flask import Flask, request, jsonify

from flask_cors import CORS
from itertools import islice

import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "backend/products.json"

@app.route('/products', methods=['GET'])
def get_products():
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            products = json.load(f)
    else:
        products = []
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    product = {data['name']: data['price']}
    products = []
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            products = json.load(f)
    products.update(product)
    with open(DATA_FILE, 'w') as f:
        json.dump(products, f)
    return jsonify({"message": "Product added!"}), 201

@app.route('/product/<int:index>', methods=['DELETE'])
def remove_product(index):
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            products = json.load(f)
        if 0 <= index < len(products):
            del products[next(islice(products, index, None))]
            with open(DATA_FILE, 'w') as f:
                json.dump(products, f)
            return jsonify({"message": "Product removed!"})
    return jsonify({"error": "Invalid index!"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
