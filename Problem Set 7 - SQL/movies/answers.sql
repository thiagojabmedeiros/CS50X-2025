SELECT title FROM movies WHERE year = 2008;

SELECT birth FROM people WHERE name = 'Emma Stone';

SELECT title FROM movies WHERE year >= 2018 ORDER BY title ASC;

SELECT COUNT(title) FROM movies JOIN ratings on movies.id = ratings.movie_id WHERE rating = 10;

SELECT title, year FROM movies WHERE title LIKE 'Harry Potter%' ORDER BY year ASC;

SELECT AVG(rating) FROM movies JOIN ratings ON movies.id = ratings.movie_id WHERE year = 2012;

SELECT title, rating FROM movies JOIN ratings ON movies.id = ratings.movie_id WHERE year = 2010 ORDER BY rating DESC, title ASC;

SELECT name FROM people JOIN stars ON people.id = stars.person_id WHERE movie_id = 114709;

SELECT DISTINCT name FROM people where id IN(SELECT person_id FROM stars WHERE movie_id IN(SELECT id FROM movies WHERE year = 2004)) ORDER BY people.birth ASC;

SELECT DISTINCT name FROM people WHERE id IN (SELECT person_id FROM directors WHERE movie_id IN (SELECT movie_id FROM ratings WHERE rating >=9));

SELECT title, rating FROM movies JOIN ratings ON movies.id = ratings.movie_id WHERE movies.id IN (SELECT movie_id FROM stars WHERE person_id = 1569276) ORDER BY rating DESC LIMIT 5;

SELECT title FROM movies WHERE id IN(SELECT movie_id FROM stars WHERE person_id = 177896) AND id IN(SELECT movie_id FROM stars WHERE person_id = 2225369) ORDER BY title ASC;

SELECT DISTINCT name FROM people WHERE id IN(SELECT person_id FROM stars WHERE movie_id IN(SELECT id FROM movies WHERE id IN(SELECT movie_id FROM stars WHERE person_id = 102)));
