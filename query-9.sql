SELECT DISTINCT subjects.name AS subject_name
FROM grades
JOIN subjects ON grades.subject_id = subjects.id
JOIN students ON grades.student_id = students.id
WHERE students.name = 'Garrett Nguyen';  