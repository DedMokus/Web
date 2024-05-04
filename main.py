from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware, db
from bert_inference import preprocess_and_inference
from processing import doPredicts
import pandas as pd
import os
from contextlib import asynccontextmanager
from db import database, metadata, engine



# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     database.connect()
#     yield
#     database.disconnect()



app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url='postgresql://postgres:postgres@localhost/vebinar_db')

#ToDo Сделать возможность отправлять и на проверку вебинары через телеграм
#     Разные возможности у юзеров разного типа

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="static"), name="templates")


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
def upload(file: UploadFile):

    print("File load")
    #Считываем выгруженный файл
    contents = file.file.read()
    #Сохраняем данные как DataFrame
    data = BytesIO(contents)
    df = pd.read_csv(data)
    data.close()
    file.file.close()
    
    return preprocess_and_inference(df)

@app.get("/general-data")
def generalData():
    #Создаем SQL запрос
    need_cols = ["Время от начала урока","Вежливость", "Технические проблемы", "Хорошее объяснение материала", "Плохое объяснение материала", "Помощь и понимание", "Реклама и спам", "Оскорбления и конфликты", "Опоздание", "Выполнение задания"]
    sql_query = "SELECT {} FROM vebinars".format(','.join([f'"{x}"' for x in need_cols]))
    print(sql_query)

    #Считываем данные из базы по запросу
    data = pd.read_sql(sql=sql_query, con=engine)

    #Делаем выводы и сохраняем статистику
    predicts_imgs = {}
    img_path = "static/images/img_general_vebinar.jpg"
    preds = doPredicts(data, img_path)
    predicts_imgs["data"] = preds
    predicts_imgs["path"] = img_path 
    return predicts_imgs

@app.get("/sep-data/")
def sepData():
    #Создаем SQL запрос
    need_cols = ["ID урока","Время от начала урока","Вежливость", "Технические проблемы", "Хорошее объяснение материала", "Плохое объяснение материала", "Помощь и понимание", "Реклама и спам", "Оскорбления и конфликты", "Опоздание", "Выполнение задания"]
    sql_query = "SELECT {} FROM vebinars".format(','.join([f'"{x}"' for x in need_cols]))
    data = pd.read_sql(sql=sql_query, con=engine)
    
    #Делаем предикты для каждого вебинара
    predicts_imgs = []
    vebin_IDs = data["ID урока"].unique()
    print(vebin_IDs)
    for group_name, group_data in data.groupby("ID урока"):
        img_path = "static/images/img_" + str(group_name) + "_vebinar.jpg"
        preds = doPredicts(group_data, img_path, group_name)
        print(preds)
        print(img_path)
        pr = {}
        pr["data"] = preds
        pr["path"] = img_path
        pr["ID"] = group_name
        
        
        predicts_imgs.append(pr)
    
    return predicts_imgs