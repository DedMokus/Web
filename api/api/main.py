from io import BytesIO
from fastapi import FastAPI, UploadFile, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware
from bert_inference import preprocess_and_inference
from processing import doPredicts
import pandas as pd
import os
from sqlalchemy.orm import Session
import models
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url='postgresql://postgres:postgres@localhost/vebinar_db')

#ToDo Сделать возможность отправлять и на проверку вебинары через телеграм
#     Разные возможности у юзеров разного типа

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    #Определяем путь к index.html
    index_path = os.path.join("templates", "index.html")
    #Открываем файл и считываем
    with open(index_path, "r") as file:
        content = file.read()
    #Возвращаем как HTML
    return HTMLResponse(content)

@app.post("/upload")
async def upload(file: UploadFile):

    print("File load start")
    #Считываем выгруженный файл
    contents = await file.file.read()
    #Сохраняем данные как DataFrame
    data = BytesIO(contents)
    df = pd.read_csv(data)
    data.close()
    file.file.close()
    preprocess_and_inference(df)
    return {"success": True}

@app.get("/general-data")
async def generalData():
    #Создаем SQL запрос
    data = pd.read_sql_table(
        "messages",
        con=engine,
        columns=["MessageID", 
                 "LessonID", 
                 "StartTime", 
                 "Message", 
                 "MessageTime", 
                 "TimeFromStart", 
                 "Polite", 
                 "TechProblems", 
                 "GoodExplain", 
                 "BadExplain", 
                 "Help", 
                 "Spam", 
                 "Conflict", 
                 "Late", 
                 "TaskComplete"]
    )
    
    #Делаем выводы и сохраняем статистику
    predicts_imgs = {}
    img_path = "static/images/img_general_vebinar.jpg"
    preds = doPredicts(data, img_path)
    predicts_imgs["data"] = preds
    predicts_imgs["path"] = img_path 
    return predicts_imgs

@app.get("/sep-data/")
async def sepData():
    #Создаем SQL запрос
    data = pd.read_sql_table(
        "messages",
        con=engine,
        columns=["MessageID", 
                 "LessonID", 
                 "StartTime", 
                 "Message", 
                 "MessageTime", 
                 "TimeFromStart", 
                 "Polite", 
                 "TechProblems", 
                 "GoodExplain", 
                 "BadExplain", 
                 "Help", 
                 "Spam", 
                 "Conflict", 
                 "Late", 
                 "TaskComplete"]
    )
    
    #Делаем предикты для каждого вебинара
    predicts_imgs = []
    vebin_IDs = data["LessonID"].unique()
    for group_name, group_data in data.groupby("LessonID"):
        img_path = "static/images/img_" + str(group_name) + "_vebinar.jpg"
        preds = doPredicts(group_data, img_path, group_name)
        pr = {}
        pr["data"] = preds
        pr["path"] = img_path
        pr["ID"] = group_name
        
        predicts_imgs.append(pr)
    
    return predicts_imgs

@app.get("/filter")
async def filter(need_class: str, id: int = None, db: Session = Depends(get_db)):

    data = pd.read_sql_table(
        "messages",
        con=engine,
        columns=["MessageID", 
                 "LessonID", 
                 "StartTime", 
                 "Message", 
                 "MessageTime", 
                 "TimeFromStart", 
                 "Polite", 
                 "TechProblems", 
                 "GoodExplain", 
                 "BadExplain", 
                 "Help", 
                 "Spam", 
                 "Conflict", 
                 "Late", 
                 "TaskComplete"]
    )
    if not id:
        filter = data[need_class] == 1
    else:
        filter = (data[need_class] == 1) & (data["LessonID"] == id)
    filtered = data[filter]
    filtered = filtered.drop(columns=["MessageID", 
                                        "LessonID", 
                                        "StartTime",
                                        "TimeFromStart", 
                                        "Polite", 
                                        "TechProblems", 
                                        "GoodExplain", 
                                        "BadExplain", 
                                        "Help", 
                                        "Spam", 
                                        "Conflict", 
                                        "Late", 
                                        "TaskComplete"
                                      ])
    filtered['MessageTime'] = filtered["MessageTime"].dt.strftime('%d/%m/%y %H:%M:%S')
    filter_json = filtered.to_dict(orient='records')

    return filter_json
