from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from models.db import Base


class Import(Base):
    __tablename__ = "imports"
    id = Column(Integer, primary_key=True, autoincrement=True)
    citizens = relationship("Citizen", backref='imports', lazy='dynamic')
