\c QUIZ

DROP TABLE IF EXISTS answers;
DROP TABLE IF EXISTS questions;

CREATE TABLE questions (
            id SERIAL PRIMARY KEY,
            number INT NOT NULL,
            subject VARCHAR NOT NULL,
            topic VARCHAR NOT NULL,
            theme VARCHAR NOT NULL,
            question VARCHAR NOT NULL,
            image BYTEA,
            image_filename VARCHAR,
            image_width VARCHAR,
            image_height VARCHAR
        );
        
CREATE TABLE answers (
            id SERIAL PRIMARY KEY,
            question_id INT REFERENCES questions(id),
            answer_no INT NOT NULL,
            answer VARCHAR NOT NULL,
            correct BOOLEAN  NOT NULL
        );