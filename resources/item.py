import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError

from schemas import ItemSchemas, ItemUpdateSchema


blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchemas)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchemas)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data

            return item
        except KeyError:
            abort(404, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchemas(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchemas)
    @blp.response(201, ItemSchemas)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item
