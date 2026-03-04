



SELECT * 
FROM movie_list
WHERE release_year > 2010;

SELECT *
FROM movie_list
WHERE genre IN('Action', 'Sci-fi');

SELECT *
FROM movie_list
WHERE title LIKE '%The%'

SELECT *
FROM movie_list
WHERE release_year BETWEEN 2008 AND 2014;

SELECT *
FROM movie_list
WHERE release_year IS NULL;