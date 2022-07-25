from sqlalchemy import  create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


CONN = "sqlite:///sqlite.db" 

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)

session = Session()
Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'Pessoa'
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    usuario = Column(String(50))
    senha = Column(String(200))


class Tokens(Base):
    __tablename__='Tokens'
    id = Column(Integer, primary_key=True)
    id_pessoa = Column(Integer, ForeignKey('Pessoa.id'))
    token = Column(String(100))
    date = Column(DateTime, default=datetime.datetime.utcnow())


Base.metadata.create_all(engine)