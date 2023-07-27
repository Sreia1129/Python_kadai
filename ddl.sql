CREATE TABLE book_user (
  id SERIAL PRIMARY KEY,
  name VARCHAR(64),
  hashed_password VARCHAR(64),
  salt VARCHAR(30)
);

CREATE TABLE book(
 id serial,
 ISBN INTEGER NOT NULL,
 name VARCHAR(30),
 author VARCHAR(16),
 publisher VARCHAR(60),
 PRIMARY KEY(id)
);
