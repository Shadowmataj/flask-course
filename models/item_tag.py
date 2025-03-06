"""Model for item-tag n:m relationship."""

from db import db


class ItemTagModel(db.Model):
    """Model for item-tag n:m relationship."""

    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
