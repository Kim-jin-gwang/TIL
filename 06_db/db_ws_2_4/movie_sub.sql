

INSERT INTO movie_list(title, genre, release_year)
VALUES
    ('The Matrix', 'Sci-Fi', 1999),
    ('Gladiator', 'Action', 2000),
    ('Jurassic Park', 'Sci-Fi', 1993),
    ('The Fugitive', 'Action', 1993);

SELECT title
FROM movie_list
WHERE genre = 'Drama' AND release_year = (
    SELECT MIN(release_year)
    FROM movie_list
    WHERE genre = 'Drama'
    );

SELECT title, release_year
FROM movie_list
WHERE genre = 'Action' AND release_year > 2000 AND release_year = (
    SELECT MAX(release_year)
    FROM movie_list
    WHERE genre = 'Action' AND release_year > 2000
);

SELECT *
FROM movie_list
WHERE genre IN ('Sci-Fi', 'Action') AND release_year IN (
    SELECT release_year
    FROM movie_list
    WHERE genre = 'Drama'
);


SELECT *
FROM movie_list
WHERE genre = 'Sci-Fi' AND release_year > (
    SELECT AVG(release_year)
    FROM movie_list
    WHERE genre = 'Action'
);

SELECT *
FROM movie_list
WHERE genre <> 'Action' AND release_year = (
    SELECT MIN(release_year)
    FROM movie_list
    WHERE genre = 'Action'
);