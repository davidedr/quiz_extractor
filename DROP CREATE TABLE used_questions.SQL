\c quiz

DROP TABLE IF EXISTS used_questions;

CREATE TABLE used_questions (
    id SERIAL PRIMARY KEY,
    theme VARCHAR NOT NULL,
    session INT NOT NULL,
    quiz_number INT NOT NULL,
    quiz_timestamp TIMESTAMP WITH TIME ZONE,
    question_id INT NOT NULL REFERENCES questions(id)    
)