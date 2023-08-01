from flask import Flask, jsonify

from flask_smorest import Api

from resources.user import blp as UserBlueprint

app = Flask(__name__)


app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Patient Management System REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = '3.0.3'
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = '/swagger-ui'
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)


api.register_blueprint(UserBlueprint)



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
