import uuid
from flask import request, jsonify

from flask.views import MethodView
from flask_smorest import Blueprint, abort


blp = Blueprint("stores", __name__, description="Operation on stores")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    def get(self, store_id):
        try: 
            return jsonify({"message": "Store by id", "store_id": store_id})
        except KeyError:
            abort(404, message="Stores not found")

    def delete(self, store_id):
        try:
            return jsonify({"message": "Store by id deleted",  "store_id": store})
        except KeyError:
            abort(404, message="Stores not found")


@blp.route('/store')
class StoreList(MethodView):
    def get(self):
        return jsonify({"message": "Stores all"})