from db import db

class UserModel(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False, unique=True)
    username = db.Column(db.String(80), nullable = False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    uploaded_files = db.relationship("UploadedFileModel", back_populates="user", lazy="dynamic", cascade="all, delete")  # delete-orphan -> Research


    # store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    # store = db.relationship("StoreModel", back_populates="items ") #in ItemModel(this)
    # items = db.relationship("ItemModel", back_populates"store, lazy="dynamic") # in storeModel


