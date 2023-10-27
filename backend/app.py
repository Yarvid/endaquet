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

@app.route('/combination', methods=['GET'])
def get_combination():
    target_sum = float(request.args.get('sum', 0))
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            products = json.load(f)

    prices_cents = [int(p * 100) for p in products.values()]
    target_sum_cents = int(target_sum * 100)
    
    combination_cents = solve_knapsack_problem(prices_cents, target_sum_cents)

    combination = [float(c / 100) for c in combination_cents]

    sub_products = {}

    for i in combination:
        for product, price in products.items():
            if price == i:
                if product in sub_products:
                    sub_products[product]['amount'] += 1
                else:
                    sub_products[product] = {
                        'price': price,
                        'amount': 1
                    }
                break

    return jsonify(sub_products) 


def solve_knapsack_problem(prices, target_sum):
    n = len(prices)
    dp = [[False for _ in range(target_sum + 1)] for _ in range(n + 1)]
    
    for i in range(n + 1):
        dp[i][0] = True
        
    for i in range(1, n + 1):
        for j in range(1, target_sum + 1):
            if prices[i - 1] <= j:
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - prices[i - 1]]
            else:
                dp[i][j] = dp[i - 1][j]

    if not dp[n][target_sum]:
        return None
    
    combination = []
    w = target_sum
    for i in range(n, 0, -1):
        if not dp[i - 1][w]:
            combination.append(prices[i - 1])
            w -= prices[i - 1]
    
    return combination

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
