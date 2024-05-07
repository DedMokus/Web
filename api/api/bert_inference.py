import pandas as pd
from transformers import pipeline
import torch
import tqdm
from db import engine
from telegramNotifications import sendNotification

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
classifier = pipeline("zero-shot-classification",
                      model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", device = device)

candidates = ["Прощание", "Спасибо", "Досвидания", "Пока", "До встречи", "Здравствуйте", 
              "Технические неполадки", "Не слышно", "Сломался микрофон", "Сломалось", "Лагает", 
              "Хорошее объяснение материла", "Теперь понял", "Понятно", "Спасибо за объяснение", 
              "Преподаватель плохо объяснил", "Повторите", "Можно ещё раз", "Не понял", 
              "Сложный материал", "Сложный урок", "Просьба о помощи", "Ссылка на сайт", 
              "Флуд, спам", "Реклама", "Спам", "Бессвязный набор букв", 
              "Оскорбление или токсичное поведение", "Ругательство", 
              "Кто-то опаздывает", "Опоздание", "Задерживается", "Готово", "Сделано", "Сдал", "Выполнил"]

# Группы кандидатов
groups = {
    "polite": ["Прощание", "Спасибо", "Досвидания", "Пока", "До встречи", "Здравствуйте"],

    "techproblems": ["Технические неполадки", "Не слышно", "Сломался микрофон", "Сломалось", "Лагает"],

    "goodexplain": ["Хорошее объяснение материла", "Теперь понял", "Понятно", "Спасибо за объяснение"],
    
    "badexplain": ["Преподаватель плохо объяснил", "Повторите", "Можно ещё раз", "Не понял", "Сложный материал", "Сложный урок"],

    "help": ["Просьба о помощи", "Ссылка на сайт"],

    "spam": ["Флуд, спам", "Реклама", "Спам", "Бессвязный набор букв"],

    "conflict": ["Оскорбление или токсичное поведение", "Ругательство"],

    "late": ["Кто-то опаздывает", "Опоздание", "Задерживается"], 
    
    "taskcomplete" : ["Готово", "Сделано", "Сдал", "Выполнил", "Код"]
}

SQLColumns = ["lessonid", "starttime", "message", "messagetime", "timefromstart", "polite", "techproblems", "goodexplain", "badexplain", "help", "spam", "conflict", "late", "taskcomplete"]

def preprocess_and_inference(train: pd.DataFrame):
    try:
        train.dropna(inplace=True)
        train["lessonid"] = train["ID урока"].astype(int)
        train['starttime'] = pd.to_datetime(train['Дата старта урока'], utc=False, errors='coerce')
        train['messagetime'] = pd.to_datetime(train['Дата сообщения'], utc = False, errors='coerce')
        train.dropna(inplace=True)
        train['timefromstart'] = ((train['messagetime'] - train['starttime']).dt.total_seconds() / 60).round(2)
        train['message'] = train["Текст сообщения"]

        group_probabilities = pd.DataFrame(0, index=range(len(train)), columns=groups.keys())
        sample_train = train.iloc[:10].reset_index(drop=True)  # Сбрасываем индексы и удаляем старые
        sample_dummy = group_probabilities.iloc[:10].reset_index(drop=True)  # Сбрасываем индексы и удаляем старые

        # Классифицируем каждую запись в train и устанавливаем 1 для группы с наибольшей вероятностью
        merged_df = pd.concat([sample_train, sample_dummy], axis=1)
        merged_df = merged_df[SQLColumns]

        for i, text in tqdm.tqdm(enumerate(merged_df['message']), total=len(merged_df)):
            classification = classifier(text, candidates)
            max_label = classification['labels'][0]  # Получаем самый вероятный класс
            for group, group_candidates in groups.items():
                if max_label in group_candidates:  # Проверяем, принадлежит ли класс кандидатам текущей группы
                    merged_df.loc[i, group] = 1

        merged_df.to_sql(name="messages", con=engine, if_exists="append", index=True, index_label="MessageID")

        text = f'''Загрузка и обработка файла размером {len(merged_df)} элементов завершена'''

        sendNotification(text)
        return 1
    except Exception as e:
        raise(e)
        return 0
    
# lass MessageSQL(Base):
#     __tablename__ = "messages"
#     MessageID = Column(Integer, primary_key=True)
#     LessonID = Column(Integer),
#     StartTime = Column(DateTime),
#     Message = Column(TEXT),
#     MessageTime = Column(DateTime),
#     TimeFromStart = Column(Float),
#     Polite = Column(Boolean),
#     TechProblems = Column(Boolean),
#     GoodExplain = Column(Boolean),
#     BadExplain = Column(Boolean),
#     Help = Column(Boolean),
#     Spam = Column(Boolean),
#     Conflict = Column(Boolean),
#     Late = Column(Boolean),
#     TaskComplete = Column(Boolean)

