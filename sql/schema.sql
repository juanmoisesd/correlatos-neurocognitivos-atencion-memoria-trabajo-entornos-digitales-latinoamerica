CREATE TABLE neurocognitive_results (
    subject_id VARCHAR(50) PRIMARY KEY,
    age INT,
    gender VARCHAR(10),
    digital_hours FLOAT,
    attention_score INT,
    wm_score INT,
    region VARCHAR(100)
);
