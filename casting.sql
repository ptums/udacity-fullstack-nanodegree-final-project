CREATE TABLE Movies (
    id SERIAL PRIMARY KEY,
    title varchar(500) NOT NULL,
    release varchar(500) NOT NULL
); 

CREATE TABLE Actors (
    id SERIAL PRIMARY KEY,
    name varchar(500) NOT NULL,
    age varchar(500) NOT NULL,
    gender varchar(500) NOT NULL,
    movie_id int NULL,
    FOREIGN KEY (movie_id) REFERENCES Movies(id)
); 

INSERT INTO Movies(title, release) VALUES('The Life Aquatic with Steve Zissou', '2004');
INSERT INTO Movies(title, release) VALUES('Dr. No', '1962');
INSERT INTO Movies(title, release) VALUES('Going My Way', '1944');
INSERT INTO Movies(title, release) VALUES('The Godfather', '1972');

INSERT INTO Actors(name, age, gender, movie_id) VALUES ('Bill Murray', '69', 'male', 1);
INSERT INTO Actors(name, age, gender, movie_id) VALUES ('Sean Connery', '89', 'male', 2);
INSERT INTO Actors(name, age, gender, movie_id) VALUES ('Bing Crosby', '74', 'male', 3);
INSERT INTO Actors(name, age, gender, movie_id) VALUES ('Al Pacino', '79', 'male', 4);