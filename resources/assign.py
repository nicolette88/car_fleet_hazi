from models.car import CarModel
from flask_restful import Resource, reqparse
from models.driver import DriverModel
from db import db


class AssignDriverToCar(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('driver_id',
                      type=str,
                      required=True,
                      help="Please enter the driver id")
  parser.add_argument('car_id',
                      type=str,
                      required=True,
                      help="Please enter the car id")

  def post(self):
    data = AssignDriverToCar.parser.parse_args()

    driver = DriverModel.find_by_id(data['driver_id'])
    if not driver:
      return {"message": "Driver does not exist"}, 404
    car = CarModel.find_by_id(data['car_id'])
    if not car:
      return {"message": "Car does not exist"}, 404
    print(car.driver_id)

    if car.driver_id == driver.id:
      return {"message": f"This assignment has already been made."}, 200

    other_driver = db.session.query(CarModel).filter(
        CarModel.driver_id == data['driver_id'],
        CarModel.id != car.id).first()

    if other_driver:
      return {"message": f"This driver is already assigned to a car"}, 405

    if car.driver_id is not None:
      return {"message": f"This car is already assigned to a driver"}, 405
    else:
      car.driver_id = driver.id
      driver.car_id = car.id
      db.session.commit()

    return {
        "message":
        f"Driver {driver.name} was assigned to car: {car.license_plate}."
    }, 201
