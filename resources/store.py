import uuid
from flask import request, jsonify

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import StoreSchema, StoreUpdateSchema


blp = Blueprint("stores", __name__, description="Operation on stores")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try: 
            return jsonify({"message": "Store by id", "store_id": store_id})
        except KeyError:
            abort(404, message="Stores not found")

    @blp.arguments(StoreUpdateSchema)
    # @blp.response(200, StoreSchema) # order matters
    def put(self, store_data, store_id ):
        try:
            store_db_data = {"id": "34", "name": "Adidas"}
            return store_db_data
        except KeyError:
            abort(404, message="Stores not found")

    def delete(self, store_id):
        try:
            return jsonify({"message": "Store by id deleted",  "store_id": store})
        except KeyError:
            abort(404, message="Stores not found")


@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        store_db_data = {"id": "34", "name": "Adidas"}
        return store_db_data

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store_db_data = {"id": "34", "name": "Adidas"}
        return store_db_data
