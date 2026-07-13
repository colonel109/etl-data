from database.controller import DatabaseController
from src.database.structure import Base
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg://postgres:duong1234@localhost:5432/daesang_db_test")
client = DatabaseController(engine)
client.create_table()