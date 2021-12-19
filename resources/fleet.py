from flask_restful import Resource
from models.fleet import FleetModel


class Fleet(Resource):
  def get(self, name):
    fleet = FleetModel.find_by_name(name)
    if fleet:
      return fleet.json()
    return {'message': 'Fleet not found'}, 404

  def post(self, name):
    if FleetModel.find_by_name(name):
      return {
          'message': "A fleet with name '{}' already exists.".format(name)
      }, 400

    fleet = FleetModel(name)
    try:
      fleet.save_to_db()
    except:
      return {"message": "An error occurred creating the fleet."}, 500

    return fleet.json(), 201

  def delete(self, name):
    fleet = FleetModel.find_by_name(name)
    if fleet:
      fleet.delete_from_db()

    return {'message': 'Fleet deleted'}


class FleetList(Resource):
  def get(self):
    return {
        'fleets': list(map(lambda car: car.json(), FleetModel.query.all()))
    }
