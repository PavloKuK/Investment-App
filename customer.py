from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///customer.db?check_same_thread=False')
Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    
    accountNumber = Column(Integer, primary_key = True)
    name = Column(String)
    bankName = Column(String)
    balance = Column(Float)
    state = Column(String)
    portfolioList = Column(String)
    portfolioValue = Column(Float)
    totalDividents = Column(Float)
    capitalGains = Column(Float)
    taxes = Column(Float)
   
   
Base.metadata.create_all(engine)
   