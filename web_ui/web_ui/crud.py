from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext


password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def getUser(db: Session, userID: int):
    return db.query(models.UserSQL).filter(models.UserSQL.userid == userID).first()

def getUserByEmail(db: Session, email: str):
    return db.query(models.UserSQL).filter(models.UserSQL.email == email).first()

def getUsers(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.UserSQL).offset(offset).limit(limit).all()

def createUser(db: Session, user: schemas.UserCreate):
    password = user.password
    hashed_password = password_context.hash(password)
    db_user = models.UserSQL(username=user.username, password=hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def getPasswordHash(password: str) -> str:
    return password_context.hash(password)

def verifyPassword(hashedPassword: str, textPassword: str):
    return password_context.verify(textPassword, hashedPassword)

def getMessages(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.MessageSQL).offset(offset).limit(limit).all()

def createMessage(db: Session, message: schemas.MessageCreate):
    db_message = models.MessageSQL(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
