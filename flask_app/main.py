from flask import Flask, jsonify, request

from shared.data import items

# Create Flask app instance
app = Flask(__name__)


# Helper to find an item by ID
def _find_item(item_id: int):
    return next((item for item in items if item['id'] == item_id), None)


# Custom error handlers for a more consistent API experience
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad Request"}), 400


@app.route('/items', methods=['GET'])
def get_items():
    """Returns the full list of items."""
    return jsonify(items)


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int):
    """Returns a single item by its ID."""
    item = _find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)


@app.route('/items', methods=['POST'])
def create_item():
    """Creates a new item."""
    data = request.get_json()
    # Basic validation
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({"error": "Missing name or description"}), 400

    # Find the highest existing ID and add 1
    new_id = max(item['id'] for item in items) + 1 if items else 1

    new_item = {
        'id': new_id,
        'name': data['name'],
        'description': data['description']
    }
    items.append(new_item)

    return jsonify(new_item), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id: int):
    """Updates an existing item."""
    item = _find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad request"}), 400

    # Update item with new data
    item['name'] = data.get('name', item['name'])
    item['description'] = data.get('description', item['description'])

    return jsonify(item)


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id: int):
    """Deletes an item."""
    item = _find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    items.remove(item)
    return jsonify({"message": "Item deleted"})
