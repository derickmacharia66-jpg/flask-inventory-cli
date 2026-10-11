from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Simulated Database
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, ...",
        "price": 3.99,
        "stock": 50
    }
]

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'product_name' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    new_item = {
        "id": inventory[-1]["id"] + 1 if inventory else 1,
        "product_name": data.get("product_name"),
        "brands": data.get("brands", ""),
        "ingredients_text": data.get("ingredients_text", ""),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0)
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    item["product_name"] = data.get("product_name", item["product_name"])
    item["brands"] = data.get("brands", item["brands"])
    item["price"] = data.get("price", item["price"])
    item["stock"] = data.get("stock", item["stock"])
    return jsonify(item), 200

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": "Item deleted successfully"}), 200

@app.route('/external-product/<barcode>', methods=['GET'])
def fetch_external_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to connect to OpenFoodFacts API"}), 502
    
    data = response.json()
    if data.get("status") != 1:
        return jsonify({"error": "Product not found on OpenFoodFacts"}), 404
        
    product = data.get("product", {})
    return jsonify({
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text")
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
    