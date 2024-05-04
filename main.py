from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from bert_inference import preprocess_and_inference
from processing import doPredicts
import pandas as pd
import os

app = FastAPI()

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
    #Считываем выгруженный файл
    contents = file.file.read()
    #Сохраняем данные как DataFrame
    data = BytesIO(contents)
    df = pd.read_csv(data)
    data.close()
    file.file.close()
    #Обрабатываем данные в модели
    preprocess_and_inference(df)
    return