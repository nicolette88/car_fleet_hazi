from db import db, BaseModel


class CarModel(BaseModel):
  __tablename__ = 'cars'
  id = db.Column(db.Integer, primary_key=True)
  license_plate = db.Column(db.String(7))
  type = db.Column(db.String(80))
  # one to one relationship
  driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), unique=True)
  driver = db.relationship('DriverModel', back_populates='car')

  # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
  positions = db.relationship('PositionModel', back_populates='car')

  # many to many
  # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
  fleets = db.relationship('CarFleetLink', back_populates='car')

  def __init__(self, plate, type):
    self.license_plate = plate
    self.type = type

  def json(self, use_fleets=True):
    car_json = {
        'license_plate': self.license_plate,
        'type': self.type,
        'car_id': self.id,
        'driver': '' if self.driver is None else self.driver.name,
    }
    if use_fleets:
      fleets = []
      for link in self.fleets:
        if link.fleet is not None:
          fleets.append(link.fleet.json(use_cars=False))
      car_json['fleets'] = fleets
    return car_json

  def save_to_db(self):
    if len(self.license_plate) > 7:
      print('license plate is too big!')
      raise Exception('Nem lehet hosszabb mint 7')
    try:
      db.session.add(self)
      db.session.commit()
    except Exception as e:
      print(f'hiba történt az adatbázisba való mentéskor: {e}')

  @classmethod
  def find_by_plate(cls, plate):
    return cls.query.filter_by(license_plate=plate).first()

  @classmethod
  def find_by_id(cls, id):
    return cls.query.filter_by(id=id).first()
