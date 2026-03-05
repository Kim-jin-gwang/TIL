


SELECT b.title AS BookTitle, a.name AS AuthorName, g.genre_name AS GenreName
FROM books b
INNER JOIN authors a ON b.author_id = a.id
INNER JOIN genres g ON b.genre_id = g.id;


CREATE INDEX idx_authors_name ON authors(name);

CREATE INDEX idx_genres_genre_name ON genres(genre_name);

SELECT b.title AS BookTitle, a.name AS AuthorName, g.genre_name AS GenreName
FROM books b
INNER JOIN authors a ON b.author_id = a.id
INNER JOIN genres g ON b.genre_id = g.id
WHERE a.name = 'J.K. Rowling' AND g.genre_name = 'Fantasy';