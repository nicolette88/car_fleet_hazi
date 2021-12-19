from db import db, BaseModel
from sqlalchemy.sql.functions import now


class PositionModel(BaseModel):
  __tablename__ = 'positions'

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime)
  latitude = db.Column(db.Float(precision=5))
  longitude = db.Column(db.Float(precision=5))
  # one to many with bidirectional relationship
  # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
  car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
  car = db.relationship('CarModel', back_populates='positions')

  def __init__(self, car_id, latitude: float, longitude: float):
    self.car_id = car_id
    self.latitude = latitude
    self.longitude = longitude
    self.date = now()

  def save_to_db(self):
    try:
      db.session.add(self)
      db.session.commit()
    except Exception as e:
      print(f'hiba történt az adatbázisba való mentéskor: {e}')
