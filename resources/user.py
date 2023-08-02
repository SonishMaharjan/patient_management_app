import uuid
from flask import request, jsonify

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity


from models import UserModel

from schemas import UserSchema, UserUpdateSchema, PlainUserSchema

from db import db

from blocklist import BLOCKLIST

blp = Blueprint("users", __name__, description="Operation on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(PlainUserSchema)
    @blp.response(201, PlainUserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.name == user_data["name"]).first():
            abort(409, message="A user already exists")
            
        user = UserModel(name=user_data["name"],
                         password= pbkdf2_sha256.hash(user_data["password"]))
        
        db.session.add(user)
        db.session.commit()
        
        return user
            
        
@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.name == user_data["name"]).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        
        abort(401, message="Invalid Credentials.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user, fresh=False)
        
        return {"access_token": new_access_token}

    
    
@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
       jti = get_jwt()["jti"]
       BLOCKLIST.add(jti)
       
       return { "message": "Successfully logged out." } 
    
    
@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        try: 
            user = UserModel.query.get_or_404(user_id)
            
            return user
        except KeyError:
            abort(404, message="users not found")

    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema) # order matters
    def put(self, user_data, user_id ):
        try:
            user = UserModel.query.get_or_404(user_id)
        
            user.name = user_data["name"]
            
            db.session.add(user)
            db.session.commit()

            return user
        except KeyError:
            abort(404, message="users not found")

    def delete(self, user_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required")
        
        
        user = UserModel.query.get_or_404(user_id)
        
        db.session.delete(user)
        db.session.commit()
        
        return {"message": "User is deleted"}, 200

        # try:
        #     return jsonify({"message": "User by id deleted",  "user_id": user_id})
        # except KeyError:
        #     abort(404, message="users not found")


@blp.route('/user')
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

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
