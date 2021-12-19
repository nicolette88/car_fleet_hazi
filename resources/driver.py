from flask_restful import Resource, reqparse
from models.driver import DriverModel


class Driver(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('name',
                      type=str,
                      required=True,
                      help="This field cannot be blank.")

  def post(self):
    data = Driver.parser.parse_args()
    driver = DriverModel(data['name'])
    driver.save_to_db()

    return {"message": "Driver created successfully."}, 201

  def get(self):
    return {"drivers": [driver.json() for driver in DriverModel.query.all()]}
