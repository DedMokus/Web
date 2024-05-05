import pandas as pd
from transformers import pipeline
import torch
import tqdm
from db import  metadata, engine

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
    "Вежливость": ["Прощание", "Спасибо", "Досвидания", "Пока", "До встречи", "Здравствуйте"],

    "Технические проблемы": ["Технические неполадки", "Не слышно", "Сломался микрофон", "Сломалось", "Лагает"],

    "Хорошее объяснение материала": ["Хорошее объяснение материла", "Теперь понял", "Понятно", "Спасибо за объяснение"],
    
    "Плохое объяснение материала": ["Преподаватель плохо объяснил", "Повторите", "Можно ещё раз", "Не понял", "Сложный материал", "Сложный урок"],

    "Помощь и понимание": ["Просьба о помощи", "Ссылка на сайт"],

    "Реклама и спам": ["Флуд, спам", "Реклама", "Спам", "Бессвязный набор букв"],

    "Оскорбления и конфликты": ["Оскорбление или токсичное поведение", "Ругательство"],

    "Опоздание": ["Кто-то опаздывает", "Опоздание", "Задерживается"], 
    
    "Выполнение задания" : ["Готово", "Сделано", "Сдал", "Выполнил", "Код"]
}

def preprocess_and_inference(train: pd.DataFrame):
    try:
        train.dropna(inplace=True)
        print(train.dtypes)
        train['Дата старта урока'] = pd.to_datetime(train['Дата старта урока'], utc=False, errors='coerce')
        train['Дата сообщения'] = pd.to_datetime(train['Дата сообщения'], utc = False, errors='coerce')
        train.dropna(inplace=True)
        train['Время от начала урока'] = ((train['Дата сообщения'] - train['Дата старта урока']).dt.total_seconds() / 60).round(2)

        group_probabilities = pd.DataFrame(0, index=range(len(train)), columns=groups.keys())
        sample_train = train.iloc[:100].reset_index(drop=True)  # Сбрасываем индексы и удаляем старые
        sample_dummy = group_probabilities.iloc[:100].reset_index(drop=True)  # Сбрасываем индексы и удаляем старые

        # Классифицируем каждую запись в train и устанавливаем 1 для группы с наибольшей вероятностью
        merged_df = pd.concat([sample_train, sample_dummy], axis=1)

        for i, text in tqdm.tqdm(enumerate(merged_df['Текст сообщения']), total=len(merged_df)):
            classification = classifier(text, candidates)
            max_label = classification['labels'][0]  # Получаем самый вероятный класс
            for group, group_candidates in groups.items():
                if max_label in group_candidates:  # Проверяем, принадлежит ли класс кандидатам текущей группы
                    merged_df.loc[i, group] = 1
        print(merged_df.columns)

        merged_df.to_sql(name="vebinars", con=engine, if_exists="replace", index=False)
        return 1
    except Exception as e:
        print(e)
        return 0
    
