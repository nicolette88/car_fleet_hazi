from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///test_db.sqlite')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  age = Column(Integer)

  def __init__(self, name):
    self.name = name

  def save_to_db(self):
    try:
      session.add(self)
      session.commit()
    except Exception as e:
      print(f'hiba történt az adatbázisba val mentéskor {e}')
    finally:
      session.close()

  @classmethod
  def find_by_id(cls, id: int):
    query = session.query(cls)
    return query.filter_by(id=id).first()


# létrehozza az adatbázist és benne a táblákat amiket definiáltunk:
Base.metadata.create_all(engine)
# new_user = User("Peter")
# new_user.age = 28
# new_user.save_to_db()
user = User.find_by_id(2)
print(user.name)