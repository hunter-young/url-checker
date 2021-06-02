from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from . database import Base

"""This module is responsible for defining the database schema. Since we define it
through ORM style, SQLAlchemy can create the actual DDL queries needed to spin up
a new database with whatever DBMS is connected"""

# database schema definitions
class CheckDefinition(Base):
    __tablename__ = 'definitions'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    frequency = Column(Integer)
    expectedStatus = Column(Integer)
    expectedString = Column(String)

    results = relationship('CheckResult', 
                           back_populates='checkDefinition', 
                           cascade='all, delete, delete-orphan')
    # relationships are used to nest entities in api output
    # they're also used enable cascade deletes
    emailAddresses = relationship('NotificationAddress', 
                                  back_populates='checkDefinition', 
                                  uselist=True,
                                  cascade='all, delete, delete-orphan', 
                                  lazy='selectin')

class CheckResult(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True, index=True)
    checkId = Column(Integer, ForeignKey('definitions.id', 
                                         ondelete='CASCADE'))
    timeChecked = Column(DateTime)
    statusCode = Column(Integer)
    state = Column(String)

    checkDefinition = relationship('CheckDefinition', 
                                   back_populates='results', 
                                   uselist=False, 
                                   lazy='selectin')

class NotificationAddress(Base):
    __tablename__ = 'notification_addresses'

    id = Column(Integer, primary_key=True, index=True)
    checkId = Column(Integer, ForeignKey('definitions.id', 
                                         ondelete='CASCADE'))
    emailAddress = Column(String)

    checkDefinition = relationship('CheckDefinition', 
                                   back_populates='emailAddresses', 
                                   uselist=False, 
                                   lazy='selectin')

