

SELECT genre
FROM movie_list
GROUP BY genre
HAVING COUNT(*) = (
    SELECT MAX(cnt)
    FROM (
        SELECT COUNT(*) AS cnt
        FROM movie_list
        GROUP BY genre
    ) AS sub
);


SELECT genre, COUNT(*) AS cnt, AVG(release_year) AS avg_genre
FROM movie_list
GROUP BY genre;


SELECT m.genre, m.title, m.release_year
FROM movie_list m
WHERE (m.genre, m.release_year) IN (
    SELECT genre, MAX(release_year)
    FROM movie_list
    GROUP BY genre
);


SELECT *
FROM movie_list
WHERE genre <> 'Action' AND release_year = (
    SELECT MIN(release_year)
    FROM movie_list
    WHERE genre = 'Action'
)
ORDER BY release_year ASC, title ASC;


SELECT *
FROM movie_list
WHERE genre IN ('Sci-Fi', 'Action') AND release_year IN (
    SELECT release_year
    FROM movie_list
    WHERE genre = 'Drama'
)
ORDER BY release_year ASC;