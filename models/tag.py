"""Tags model"""

from db import db


class TagModel(db.Model):
    """Tags model."""

    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
