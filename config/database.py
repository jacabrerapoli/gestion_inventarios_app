from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:jaca57688@localhost:3306/gestion_inventarios_db"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = Session()
