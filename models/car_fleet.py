from models.model_mixin import MixinModel
from db import BaseModel, db


class CarFleetLink(BaseModel, MixinModel):
  __tablename__ = 'car_fleet'
  car_id = db.Column(db.ForeignKey('cars.id'), primary_key=True)
  fleet_id = db.Column(db.ForeignKey('fleets.id'), primary_key=True)
  car = db.relationship('CarModel', back_populates='fleets')
  fleet = db.relationship('FleetModel', back_populates='cars')

  def __init__(self, car_id, fleet_id):
    self.car_id = car_id
    self.fleet_id = fleet_id
