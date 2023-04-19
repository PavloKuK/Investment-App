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
   
class Balance(Base):
    __tablename__ = 'balance'
    key = Column(Integer, primary_key = True)
    bank = Column(String)
    amount = Column(Float)
   
class Holdings(Base):
    __tablename__ = 'holdings'
    key = Column(Integer, primary_key = True)
    name = Column(String)
    value = Column(Float)
    gain = Column(Float)
    
class Portfolio(Base):
    __tablename__ = 'portolio'
    key = Column(Integer, primary_key = True)
    value = Column(Float)   #The current value of all companies a customer has invested
    gains = Column(Float)   #The change in value of all companies since shares were purchased in $ amount
    returns = Column(Float) #The change in value of all companies since shares were purchased in % amount
    dividents = Column(Float) #The amount of dividents that have been paid out to the customer since the stock purchase

Base.metadata.create_all(engine)
   
