"""
Resource to handle tags endpoints.
It works with:
flask_smorest to create blueprints, routes, 
arguments and responses (the last two based on schemas).
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    """Class to handle tags in a store."""

    @jwt_required()
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        """Endpoint to get all the tags in a store."""
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        """Endpoint to post a tag into the db."""
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag


@blp.route("/tags")
class TagsList(MethodView):
    """Class to get all the tags."""

    @jwt_required()
    @blp.response(200, TagSchema(many=True))
    def get(self):
        """Endpoint to retrieve all the tags."""
        return TagModel.query.all()


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    """Class to handle item tag link."""

    @jwt_required()
    @blp.response(200, TagSchema)
    def post(self, item_id, tag_id):
        """Endpoint to link an item and a tag."""
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store.id != tag.store.id:
            abort(
                400,
                message="Make sure item and tag belong to the same store before linking.",
            )

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error ocurred while inserting the tag.")
        return tag

    @jwt_required()
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        """Endpoint to unlink an item and a tag."""
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.delete(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error ocurred while deleting the tag.")
        return {"message": "Item removed from tags.", "item": item, "tag": tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    """Clas to handle get and delete by tag id."""

    @jwt_required()
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        """Endpoint to get a specific tag."""
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required()
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Return if the tag is assigned to\
            one o more items, in this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        """Endpoint to delete a specific tag."""
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag, Make sure tag is not associatedwith any item.",
        )
