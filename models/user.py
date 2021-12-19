from models.model_mixin import MixinModel
from db import BaseModel, db


class UserModel(BaseModel, MixinModel):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80))
  password = db.Column(db.String(80))

  def __init__(self, username, password):
    self.username = username
    self.password = password
