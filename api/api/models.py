from sqlalchemy import Boolean, Integer, Float, TEXT, Column, String, DateTime
from sqlalchemy.orm import relationship

from db import Base

class UserSQL(Base):
    __tablename__ = "users"
    userID = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    isAdmin = Column(Boolean, default=False)
    #isNotifications = Column(Boolean, default=False)
    #TelegramID = Column(Integer, default=None)

class MessageSQL(Base):
    __tablename__ = "messages"
    MessageID = Column(Integer, primary_key=True)
    LessonID = Column(Integer),
    StartTime = Column(DateTime),
    Message = Column(TEXT),
    MessageTime = Column(DateTime),
    TimeFromStart = Column(Float),
    Polite = Column(Boolean),
    TechProblems = Column(Boolean),
    GoodExplain = Column(Boolean),
    BadExplain = Column(Boolean),
    Help = Column(Boolean),
    Spam = Column(Boolean),
    Conflict = Column(Boolean),
    Late = Column(Boolean),
    TaskComplete = Column(Boolean)

