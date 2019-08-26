import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(DB_PATH)
engine = create_engine('sqlite://///' + DB_PATH + '/test.db', echo=True)
# create a configured "Session" class
Session = sessionmaker(bind=engine)
# create a Session
Base = declarative_base()


from models.citizen_data import CitizenRelationship
from models.citizen_data import Citizen
from models.imports import Import

Base.metadata.create_all(engine)
session = Session()
