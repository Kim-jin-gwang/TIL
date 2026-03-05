

SELECT comment
from feedback
WHERE student_id = (
    SELECT id
    FROM students
    WHERE username = 'john_doe'
)
ORDER BY created_at ASC
LIMIT 1;

CREATE VIEW student_feedback_with_courses AS
SELECT s.username, c.title AS course_title, f.comment, f.created_at
FROM feedback f
INNER JOIN students s ON f.student_id = s.id
INNER JOIN courses c ON f.course_id = c.id;


SELECT *
FROM student_feedback_with_courses
WHERE username = 'john_doe'