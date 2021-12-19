from models.model_mixin import MixinModel
from db import db, BaseModel
# to avoid circular import
import models.car


class DriverModel(BaseModel, MixinModel):
  __tablename__ = 'drivers'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  # one to one relationship:
  # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-one
  car = db.relationship('CarModel', back_populates='driver', uselist=False)

  # car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), unique=True)

  def json(self):
    car = models.car.CarModel.query.filter_by(driver_id=self.id).first()
    return {"name": self.name, "car": False if car is None else car.type}

  def __init__(self, name):
    self.name = name

  @classmethod
  def find_by_id(cls, id):
    return cls.query.filter_by(id=id).first()
