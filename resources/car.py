from flask_restful import Resource, reqparse
from models.car import CarModel
from flask_jwt import jwt_required


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
    if CarModel.find_by_plate(plate):
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
    car = CarModel.find_by_plate(plate)
    if car:
      return car.json()
    return {'message': 'car not found'}, 404
