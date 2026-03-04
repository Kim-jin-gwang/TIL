



SELECT *
FROM movie_list
WHERE release_year BETWEEN 2000 AND 2010

SELECT *
FROM movie_list
WHERE title >= 'A' AND title < 'N';

SELECT *
FROM movie_list
WHERE genre = 'Drama' AND release_year BETWEEN 190 AND 2000

SELECT *
FROM movie_list
WHERE release_year BETWEEN 2015 AND 2020 AND genre IN ('Sci-fi', 'Action');

SELECT *
FROM movie_list
WHERE release_year BETWEEN 2006 AND 2014;