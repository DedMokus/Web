from sqlalchemy import Boolean, Integer, Float, TEXT, Column, String, DateTime
from sqlalchemy.orm import relationship

from db import Base

class UserSQL(Base):
    __tablename__ = "users"
    userid = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    isadmin = Column(Boolean, default=False)
    #isNotifications = Column(Boolean, default=False)
    #TelegramID = Column(Integer, default=None)

class MessageSQL(Base):
    __tablename__ = "messages"
    messageid = Column(Integer, primary_key=True)
    lessonid = Column(Integer),
    starttime = Column(DateTime),
    message = Column(TEXT),
    messagetime = Column(DateTime),
    timefromstart = Column(Float),
    polite = Column(Boolean),
    techproblems = Column(Boolean),
    goodexplain = Column(Boolean),
    badexplain = Column(Boolean),
    help = Column(Boolean),
    spam = Column(Boolean),
    conflict = Column(Boolean),
    late = Column(Boolean),
    taskcomplete = Column(Boolean)

