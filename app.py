import os

from flask import Flask, jsonify

from flask_smorest import Api


from flask_jwt_extended import JWTManager

from db import db



import models

from resources.user import blp as UserBlueprint
from resources.uploaded_file import blp as UploadedFileBlueprint

def create_app(db_url=None):    
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Patient Management System REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = '3.0.3'
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = '/swagger-ui'
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)
    
    app.config["JWT_SECRET_KEY"] = "my-jwt-secret-key" # secrets.SystemRandom().getrandbits(128)
    jwt = JWTManager(app)
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "The token has expired.", "error": "token_expired"}), 401)
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify(
                    {
                        "description": "Request does not contain an access token.",
                        "error": "authorization_required"
                    }
                    ),
                401)
        
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify( 
                    {
                        "description": "Request doen not contain an acces token",
                        "error": "authorization_required"
                    }),
            401
        )
    

    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(UploadedFileBlueprint)

    return app

# Sample data to be returned as JSON
# sample_data = {
#     "message": "Hello, this is a simple Flask API!",
#     "data": [1,4, 5]
# }

# @app.route('/')
# def hello():
#     return jsonify(sample_data)

# if __name__ == '__main__':
#     app.run(debug=True)
