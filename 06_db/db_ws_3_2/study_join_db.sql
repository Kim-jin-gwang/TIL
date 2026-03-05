


SELECT s.username, c.title, f.comment
FROM feedback f
INNER JOIN students s ON f.student_id = s.id
INNER JOIN courses c ON f.course_id = c.id
WHERE s.username = 'john_doe';

SELECT s.username, c.title, f.comment
FROM feedback f
LEFT JOIN students s ON f.student_id = s.id
LEFT JOIN courses c ON f.course_id = c.id
WHERE s.username = 'jane_smith';

SELECT f.comment
FROM feedback f
INNER JOIN students s ON f.student_id = s.id
WHERE s.username = 'mary_jones'
ORDER BY f.created_at DESC
LIMIT 1;