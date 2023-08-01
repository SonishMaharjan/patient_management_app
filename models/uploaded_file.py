from db import db

class UploadedFileModel(db.Model):
    __tablename__ = "uploaded_files"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable =  False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)

    user = db.relationship("UserModel", back_populates="uploaded_files")




