from pydantic import BaseModel
from typing import Union
from datetime import datetime

class UserBase(BaseModel):
    username: str | None = None
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    userID: int
    isAdmin: bool

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    LessonID: int
    StartTime: datetime
    Message: str
    MessageTime: datetime
    TimeFromStart: float
    Polite: bool
    TechProblems: bool
    GoodExplain: bool
    BadExplain: bool
    Help: bool
    Spam: bool
    Conflict: bool
    Late: bool
    TaskComplete: bool

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    MessageID: int

    class Config:
        orm_mode = True

