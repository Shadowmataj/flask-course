"""
Resource to handle stores endpoints.
It works with:
flask_smorest to create blueprints, routes, 
arguments and responses (the last two based on schemas).
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt
from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores.")


@blp.route("/stores")
class StoresList(MethodView):
    """Class to get all the stores."""

    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """Endpoint to retrieve all the stores."""
        return StoreModel.query.all()


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    """Class to handle get and delete by store id."""

    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """Endpoint to get a specific store."""
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self, store_id):
        """Endpoint to delete a store."""
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}


@blp.route("/store")
class StorePost(MethodView):
    """Class to post a new store."""

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        """Endpoint to post a store into the db."""
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error has ocurred while inserting the item.")
        return store
