"""Resource to handle store endpoints."""

import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores.")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    """Class to handle get and delete by store id."""
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """Method to get a specific store."""
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        """Method to delete a store."""
        try:
            del stores[store_id]
            return {"status": "success", "payload": "Store deleted."}
        except KeyError:
            abort(400, message="Store not found.")

@blp.route("/stores")
class StoreList(MethodView):
    """Class to handle get and delete by store id."""
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """Method to retrieve all the stores."""
        return stores.values()

@blp.route("/store")
class StorePost(MethodView):
    """Class to post a new store."""
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        """Method to post a photo into the db."""
        if "name" not in store_data:
            abort(400, message="Ensure 'name' is included in the JSON payload.")

        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="The store already exists.")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store
