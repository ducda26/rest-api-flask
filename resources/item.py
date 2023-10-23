import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError

from schemas import ItemSchemas, ItemUpdateSchema


blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchemas)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchemas)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id = item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        
        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchemas(many=True))
    def get(self):
        return ItemModel.query.all()
    
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
