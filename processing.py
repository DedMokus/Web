import matplotlib.pyplot as plt
import pandas as pd

def doPredicts(data, path, title=None):
    
    columns = ["MessageID", "LessonID", "StartTime", "Message", "MessageTime", "TimeFromStart", "Polite", "TechProblems", "GoodExplain", "BadExplain", "Help", "Spam", "Conflict", "Late", "TaskComplete"]
    col_check = ["Polite", "TechProblems", "GoodExplain", "BadExplain", "Help", "Spam", "Conflict", "Late", "TaskComplete"]

    if not title:
        title = "Общая статистика"
    else:
        title = f"Статистика по вебинару {title}"

    data['count'] = data[col_check].sum(axis=1)
    
    categories = pd.DataFrame({'Category': data[col_check].apply(lambda row: row.idxmax(), axis=1)})
    data = pd.concat([data, categories], axis=1)
    row = data[col_check + ["count"]].sum().to_dict()
    predicts = []
    count = row["count"]
    if row["Late"]/count > 0.2:
        predicts.append("Ученики опаздывают")
    if row["Spam"]/count > 0.15:
        predicts.append("Ученики общаются на отвлеченные темы, не заинтересованы")
    if row["TaskComplete"] > 1:
       predicts.append("Ученики выполняют небольшие задания преподавателя")
    if row["Polite"]/count > 0.2:
        predicts.append("Ученики вежливы друг с другом и преподавателем")
    if row["TechProblems"] > 1:
        predicts.append("Во время вебинара были техничесике неполадки")
    if row["Conflict"] > 0:
        predicts.append("Есть токсичные ученики, нужно следить")
    if row["Help"]/count > 0.2:
        predicts.append("Сильная взаимопомощь в команде вебинара")
    if row["GoodExplain"]/count > 0.3:
        predicts.append("Вебинар оставил хорошее впечатление")
    if row["BadExplain"]/count > 0.2:
        predicts.append("Преподаватель плохо объясняет или тема сложная")
    if data['TimeFromStart'].max() < 10:
        predicts.append("Вебинар закончился слишком рано. Вероятно произошли технические неполадки, либо пришло слишком мало учеников")

    colors = ["blue", "red", "black", "pink","magenta", "green", "grey", "yellow", "brown"]
    names = ["Вежливость", "Технические проблемы", "Хорошее объяснение материала", "Плохое объяснение материала", "Помощь и понимание", "Реклама и спам", "Оскорбления и конфликты", "Опоздание", "Выполнение задания"]

    x = [list(data[data["Category"] == category]['TimeFromStart']) for category in col_check]

    plt.switch_backend("agg")
    fig, ax = plt.subplots(figsize=(20,15))


    ax.hist(x, bins=20, color=colors, stacked=True, label=names)
    ax.set_position([0.1,0.1,0.65,0.8])
    plt.xlabel("Время с начала занятия")
    plt.title(title)
    plt.ylabel("Количество сообщений")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(path, format="jpg", dpi=70)

    return ', '.join(predicts)
