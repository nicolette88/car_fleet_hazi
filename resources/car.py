from flask_restful import Resource, reqparse
from models.car import CarModel
from models.position import PositionModel
from flask_jwt import jwt_required


class CarPosition(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('latitude',
                      type=float,
                      required=True,
                      help='The latitude field can not be blank!')
  parser.add_argument('longitude',
                      type=float,
                      required=True,
                      help='The longitude field can not be blank!')

  def get(self, plate):
    if (CarModel.find_by_attributes(license_plate=plate)) is None:
      return {'message': f'The {plate} plate is not exists'}, 404
    car = CarModel.find_by_attributes(license_plate=plate)
    car_positions = []
    for pos_data in PositionModel.query.all():
      tmp_data = pos_data.json()
      if car.id == tmp_data['car_id']:
        # mivel a JSON-nál úgy döntöttem hogy mindent visszadok, mert 'car_id'-t is szűrésre használom, így új listát hozok létre a megjelenítésre
        car_positions.append({
            'longitude': tmp_data['longitude'],
            'latitude': tmp_data['latitude'],
            'date': tmp_data['date']
        })
    return {'car_positions': car_positions}

  def post(self, plate):
    if (CarModel.find_by_attributes(license_plate=plate)) is None:
      return {'message': f'The {plate} plate is not exists'}, 404
    # létező autó és rendszám esetén:
    data = CarPosition.parser.parse_args()
    car = CarModel.find_by_attributes(license_plate=plate)
    car_position = PositionModel(car.id, data['latitude'], data['longitude'])
    try:
      car_position.save_to_db()
    except Exception:
      return {'message': 'error during database communication...'}, 400
    return {'message': 'car_position is saved to database...'}, 201


class CarList(Resource):
  def get(self):
    # cars = []
    # for car in CarModel.query.all():
    #   cars.append(car.json())
    # return {'cars': cars}
    return {'cars': [car.json() for car in CarModel.query.all()]}


class Car(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('type',
                      type=str,
                      required=True,
                      help='The type field can not be blank!')

  def post(self, plate):
    if CarModel.find_by_attributes(license_plate=plate):
      return {'message': f'This car with plate {plate} already exists'}, 400
    data = Car.parser.parse_args()
    car = CarModel(plate, data['type'])
    try:
      car.save_to_db()
    except Exception:
      return {'message': 'error during database communication...'}, 400
    return car.json(), 201

  @jwt_required()
  def get(self, plate):
    car = CarModel.find_by_attributes(license_plate=plate)
    if car:
      return car.json()
    return {'message': 'car not found'}, 404
