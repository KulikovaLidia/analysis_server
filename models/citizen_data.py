import datetime
import enum

from sqlalchemy import ForeignKey, Column, Integer, String, Enum, Date, Table
from sqlalchemy.orm import relationship, backref

from models.db import Base


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"


CitizenRelationship = Table(
    'relatives', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('citizen_id', Integer, ForeignKey('citizens.id')),
    Column('relative_id', Integer, ForeignKey('citizens.id'))
)


class Citizen(Base):
    __tablename__ = 'citizens'
    RELATIONSHIPS_TO_DICT = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    citizen_id = Column(Integer, nullable=False)
    town = Column(String(256), nullable=False)
    street = Column(String(256), nullable=False)
    building = Column(String(256), nullable=False)
    apartment = Column(Integer, nullable=False)
    name = Column(String(256), nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    import_id = Column(Integer, ForeignKey('imports.id'))
    relatives = relationship(
        'Citizen',
        secondary=CitizenRelationship,
        primaryjoin=id == CitizenRelationship.c.citizen_id,
        secondaryjoin=id == CitizenRelationship.c.relative_id,
        backref=backref('relative')
    )

    def __init__(self, data):
        self.citizen_id = data['citizen_id']
        self.town = data['town']
        self.street = data['street']
        self.building = data['building']
        self.apartment = data['apartment']
        self.name = data['name']
        self.birth_date = datetime.datetime.strptime(data['birth_date'], '%d.%m.%Y').date()
        self.gender = Gender(data['gender'])

    def as_dict(self):
        dictionary = {}
        for c in self.__table__.columns:
            if c.name == 'gender':
                dictionary[c.name] = Gender(getattr(self, c.name)).value
            elif c.name == 'birth_date':
                dictionary[c.name] = datetime.datetime.strftime(getattr(self, c.name), '%d.%m.%Y')
            else:
                dictionary[c.name] = getattr(self, c.name)
        dictionary["relatives"] = []
        for item in self.relatives:
            dictionary["relatives"].append(item.citizen_id)
        print(dictionary)
        return dictionary
