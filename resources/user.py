import uuid
from flask import request, jsonify

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import UserModel

from schemas import UserSchema, UserUpdateSchema

from db import db

from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("users", __name__, description="Operation on users")

@blp.route('/user/<string:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        try: 
            return jsonify({"message": "User by id", "user_id": user_id})
        except KeyError:
            abort(404, message="users not found")

    @blp.arguments(UserUpdateSchema)
    # @blp.response(200, UserSchema) # order matters
    def put(self, user_data, user_id ):
        try:
            user_db_data = {"id": "34", "name": "Adidas"}
            return user_db_data
        except KeyError:
            abort(404, message="users not found")

    def delete(self, user_id):
        try:
            return jsonify({"message": "User by id deleted",  "user_id": user_id})
        except KeyError:
            abort(404, message="users not found")


@blp.route('/user')
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        user_db_data = [{"id": "34", "name": "Adidas"}]
        return user_db_data

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)
        
        try: 
            db.session.add(user)
            db.session.commit()
            
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting items.")
            
        return user
