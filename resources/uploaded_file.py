from flask import request, jsonify

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import UploadedFileModel

from schemas import UploadedFileSchema, UploadedFileUpdateSchema

from db import db

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from flask_jwt_extended import jwt_required

blp = Blueprint("uploaded_files", __name__, description="Operation on uploaded file")



@blp.route('/uploaded-file/<string:uploaded_file_id>')
class User(MethodView):
    @blp.response(200, UploadedFileSchema)
    def get(self, uploaded_file_id):
        try: 
            uploaded_file = UploadedFileModel.query.get_or_404(uploaded_file_id)
            
            return uploaded_file
        except KeyError:
            abort(404, message="uploaded_files not found")

    @blp.arguments(UploadedFileUpdateSchema)
    @blp.response(200, UploadedFileSchema) # order matters
    def put(self, uploaded_file_data, uploaded_file_id ):
        try:
            uploaded_file = UploadedFileModel.query.get_or_404(uploaded_file_id)
            
            # if uploaded_file:
            uploaded_file.name = uploaded_file_data.name
            # else:
            #     uploaded_file = UploadedFileModel(**uploaded_file_data)       

            return uploaded_file
        except KeyError:
            abort(404, message="uploaded_files not found")

    def delete(self, uploaded_file_id):
        uploaded_file = UploadedFileModel.query.get_or_404(uploaded_file_id)

        raise NotImplementedError("Deleteing uploaded_file is not implemented")
        # try:
        #     return jsonify({"message": "uploaded_file by id deleted",  "uploaded_file_id": user_id})
        # except KeyError:
        #     abort(404, message="users not found")




@blp.route('/uploaded-file')
class UploadedFileList(MethodView):
    @jwt_required()
    @blp.response(200, UploadedFileSchema(many=True))
    def get(self):
        return UploadedFileModel.query.all()

    # @jwt_required(fresh=True): if always new token is required.
    @jwt_required()
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
