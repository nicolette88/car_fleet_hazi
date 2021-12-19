from models.model_mixin import MixinModel
from db import BaseModel, db


class FleetModel(BaseModel, MixinModel):
  __tablename__ = 'fleets'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))

  cars = db.relationship('CarFleetLink', back_populates='fleet')

  def __init__(self, name):
    self.name = name

  def json(self, use_cars=True):
    fleet = {'name': self.name}
    if use_cars:
      cars = []
      for link in self.cars:
        if link.car is not None:
          cars.append(link.car.json(use_fleets=False))
      fleet['cars'] = cars
    return fleet
