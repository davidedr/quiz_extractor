\c quiz

DROP TABLE IF EXISTS used_questions;

CREATE TABLE used_questions (
    id SERIAL PRIMARY KEY,
    question_id INT NOT NULL REFERENCES questions(id),
    session INT NOT NULL,
    used TIMESTAMP WITH TIME ZONE
)