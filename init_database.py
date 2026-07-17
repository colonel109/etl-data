from src.database.structure import Base, Transactions, TransactionsDaily, TransactionsStaging, Scenario
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg://postgres:duong1234@localhost:5432/daesang_db_test")

Base.metadata.create_all(bind=engine, tables=[Scenario.__table__, TransactionsStaging.__table__, Transactions.__table__, TransactionsDaily.__table__])