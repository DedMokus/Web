from fastapi import FastAPI, UploadFile, HTTPException, Depends, Request, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import requests
from sqlalchemy.orm import Session
import crud, schemas
from db import SessionLocal




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.add_middleware(DBSessionMiddleware, db_url='postgresql://postgres:postgres@db/vebinar_db')

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node_modules")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    #Определяем путь к index.html
    index_path = "index.html"
    #Открываем файл и считываем
    with open(index_path, "r") as file:
        content = file.read()
    #Возвращаем как HTML
    return HTMLResponse(content)

@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    api_url = "http://api:8001/upload"
    file_to_api = {'file': file.file.read()}
    req = requests.post(api_url, files=file_to_api)

    if req.status_code == 200:
        return {"success": True}

@app.get("/general-data")
async def generalData(request: Request):
    api_url = "http://api:8001/general-data"

    req = requests.get(api_url)

    if req.status_code == 200:
        data = req.json()
        return data


@app.get("/sep-data/")
async def sepData():

    api_url = "http://api:8001/sep-data"

    req = requests.get(api_url)

    if req.status_code == 200:
        #data = req.json()
        print(req)
        return req


@app.post("/login")
async def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.getUserByEmail(db, user.email)
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Неправильное имя пользователя или пароль")
    if not crud.verifyPassword(db_user.password, user.password):
        raise HTTPException(status_code=403, detail="Неправильное имя пользователя или пароль")
    else:
        requestUser = {'username': db_user.username,
                   'email': db_user.email}
        return {'success': True, "user": requestUser}

@app.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.getUserByEmail(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Такой пользователь уже существует")
    crud.createUser(db=db, user=user)
    return {'success':True}


@app.get("/filter")
async def filter(need_class: str, id: int = None):
    api_url = f"http://api:8001/filter?need_class={need_class}&id={id}"

    req = requests.get(api_url)

    if req.status_code == 200:
        data = req.json()
        return data
