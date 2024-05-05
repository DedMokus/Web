from sqlalchemy import (Column, Integer, MetaData, Table,
                        create_engine, TIMESTAMP, TEXT, Boolean, Float, String)

from databases import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://postgres:postgres@localhost/vebinar_db'

engine = create_engine(DATABASE_URL)
metadata = MetaData()

vebinars = Table(
    'vebinars',
    metadata,
    Column('ID урока', Integer, primary_key=True),
    Column('Дата старта урока', TIMESTAMP),
    Column('Текст сообщения', TEXT),
    Column('Дата сообщения', TIMESTAMP),
    Column("Время от начала урока", Float),
    Column('Вежливость', Boolean),
    Column("Технические проблемы", Boolean),
    Column("Хорошее объяснение материала", Boolean),
    Column("Плохое объяснение материала", Boolean),
    Column("Помощь и понимание", Boolean),
    Column("Реклама и спам", Boolean),
    Column("Оскорбления и конфликты", Boolean),
    Column("Опоздание", Boolean),
    Column("Выполнение задания", Boolean)
)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    Username = Column(String, primary_key=True)
    Password = Column(String)
    IsAdmin = Column(Boolean)
