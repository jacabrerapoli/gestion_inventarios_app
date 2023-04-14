from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

USER_DB = environ.get("USER_DB")
PASSWORD_DB = environ.get("PASSWORD_DB")
DATABASE_DB = environ.get("DATABASE_DB")
HOST_DB = environ.get("HOST_DB")
PORT_DB = environ.get("PORT_DB")

DATABASE_URL = f"mysql+pymysql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{DATABASE_DB}"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = Session()
