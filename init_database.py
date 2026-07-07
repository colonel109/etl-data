from src.database.client import DatabaseClient
from src.database.structure import Base

client = DatabaseClient()
client.create_table()