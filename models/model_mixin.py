from db import db


class MixinModel():
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def find_by_attributes(cls, **kwargs):
    return cls.query.filter_by(**kwargs).first()
