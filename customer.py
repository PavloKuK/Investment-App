from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table

engine = create_engine('sqlite:///customer.db?check_same_thread=False')
Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    
    accountNumber = Column(Integer, primary_key = True)
    name = Column(String)
    email = Column(String)
    bank = Column(String)
    address = Column(String)
    state = Column(String)
    # balance = Column(Float)
    #portfolioValue = Column(Float)
    #totalDividents = Column(Float)
    #capitalGains = Column(Float)
    #taxes = Column(Float)
    
class Credentials(Base):
    __tablename__ = 'credentials'
    key = Column(Integer, primary_key = True)
    email = Column(String)
    password = Column(String)
   
   
Base.metadata.create_all(engine)
   