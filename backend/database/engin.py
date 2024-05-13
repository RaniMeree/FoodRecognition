from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker,relationship
import os

SQLALCHMY_DATABASE_URL = 'sqlite:///database/storeDB.db'
engin = create_engine(SQLALCHMY_DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False,autoflush=False , bind=engin)

Base = declarative_base()

