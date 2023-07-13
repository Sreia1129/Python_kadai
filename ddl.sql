CREATE TABLE user_sample (
  id SERIAL PRIMARY KEY,
  name VARCHAR(64),
  hashed_password VARCHAR(64),
  salt VARCHAR(30)
);

