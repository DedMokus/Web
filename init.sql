create table messages(
    MessageID integer primary key,
    LessonID integer,
    StartTime timestamp,
    Message text,
    MessageTime timestamp,
    TimeFromStart decimal,
    Polite boolean,
    TechProblems boolean,
    GoodExplain boolean,
    BadExplain boolean,
    Help boolean,
    Spam boolean,
    Conflict boolean,
    Late boolean,
    TaskComplete boolean
)

