from src.database.structure import Base, TeamStaging, BusinessPartnerStaging
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg://postgres:duong1234@localhost:5432/daesang_db_test")

Base.metadata.create_all(bind=engine, tables=[BusinessPartnerStaging.__table__])