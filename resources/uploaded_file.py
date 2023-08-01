from flask import request, jsonify

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import UploadedFileModel

from schemas import UploadedFileSchema

from db import db

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("uploaded_files", __name__, description="Operation on uploaded file")

@blp.route('/uploaded-file')
class UploadedFileList(MethodView):
    @blp.response(200, UploadedFileSchema(many=True))
    def get(self):
        user_db_data = [{"id": "34", "name": "Adidas"}]
        return user_db_data

    @blp.arguments(UploadedFileSchema)
    @blp.response(201, UploadedFileSchema)
    def post(self, uploaded_file):
        uploaded_file = UploadedFileModel(**uploaded_file)
        
        try: 
            db.session.add(uploaded_file)
            db.session.commit()
            
        except IntegrityError:
            abort(400, message="A file name already exists.")
            
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting items.")
            
        return uploaded_file
