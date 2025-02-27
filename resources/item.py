"""Resource to handle items endpoints."""

import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items, stores
from schemas import ItemSchema, UpdateItemSchema

blp = Blueprint("items", __name__, description="Operations on items.")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    """Class to get, put and delete a specific item."""
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """Method to retrieve one item."""
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(UpdateItemSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        """Method to update an specific item."""
        if "name" not in item_data or "price" not in item_data:
            abort(400, message="Ensure 'name', and 'price' are in the JSON.")
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        """Method to delete an item."""
        try:
            del items[item_id]
            return {"status": "success", "payload": "Item deleted."}
        except KeyError:
            abort(400, message="Item not found.")

@blp.route("/items")
class ItemsList(MethodView):
    """Class to get all the items"""
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """Method to retrieve all the items."""
        return items.values()

@blp.route("/item")
class  PostItem(MethodView):
    """Class to post an item."""
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        """Method to post an items."""
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exists.")

        if item_data["store_id"] not in stores:
            abort(404, message="Store not found.")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item
