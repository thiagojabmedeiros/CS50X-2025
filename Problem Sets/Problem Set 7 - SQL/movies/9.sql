SELECT DISTINCT name FROM people where id IN(SELECT person_id FROM stars WHERE movie_id IN(SELECT id FROM movies WHERE year = 2004)) ORDER BY people.birth ASC;
