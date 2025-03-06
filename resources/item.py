"""
Resource to handle items endpoints.
It works with:
flask_smorest to create blueprints, routes, 
arguments and responses (the last two based on schemas).
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import ItemModel
from schemas import ItemSchema, UpdateItemSchema

blp = Blueprint("items", __name__, description="Operations on items.")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    """Class to get, put and delete a specific item."""

    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """Endpoint to retrieve one item."""
        item = ItemModel.query.get_or_404(item_id)
        return item
    @jwt_required()
    @blp.arguments(UpdateItemSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        """Endpoint to update an specific item."""
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        return item

    @jwt_required()
    def delete(self, item_id):
        """Endpoint to delete an item."""
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(400, message="Admin privilege required.")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}


@blp.route("/items")
class ItemsList(MethodView):
    """Class to get all the items"""
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """Endpoint to retrieve all the items."""
        return ItemModel.query.all()


@blp.route("/item")
class PostItem(MethodView):
    """Class to post an item."""
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        """Endpoint to post an items."""
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has ocurred while inserting the item.")

        return item
