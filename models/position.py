from db import db, BaseModel
from sqlalchemy.sql.functions import now
from models.model_mixin import MixinModel
# ahogy jeleztem az importnál valamilyen okból a következő üzenetet dobja a VSC: Import "geopy.geocoders" could not be resolved
# lehet a VSC-ban valamelyik bővítmény okozza nem jöttem rá. :(  A működést nem befolyásolja. :)
from geopy.geocoders import Nominatim


class PositionModel(BaseModel, MixinModel):
  __tablename__ = 'positions'

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime)
  latitude = db.Column(db.Float(precision=5))
  longitude = db.Column(db.Float(precision=5))
  address = db.Column(db.String(300))
  # one to many with bidirectional relationship
  # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
  car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
  car = db.relationship('CarModel', back_populates='positions')

  def __init__(self, car_id, latitude: float, longitude: float):
    self.car_id = car_id
    self.latitude = latitude
    self.longitude = longitude
    self.date = now()
    self.address = self.resolve_address(latitude, longitude)

  def save_to_db(self):
    try:
      db.session.add(self)
      db.session.commit()
    except Exception as e:
      print(f'hiba történt az adatbázisba való mentéskor: {e}')

  def json(self):
    car_position_json = {
        'id': self.id,
        'date': self.date.isoformat(),
        'latitude': self.latitude,
        'longitude': self.longitude,
        'address': self.address,
        'car_id': self.car_id,
    }
    return car_position_json

  # A megoldáshoz a geopy Nominatim API-t használtam:
  # https://geopy.readthedocs.io/en/stable/
  def resolve_address(self, latitude, longitude):
    locator = Nominatim(user_agent="Geodecoder")
    coordinates = str(latitude) + ", " + str(longitude)
    location = locator.reverse(coordinates)
    if location:
      return location.address
    return ""
