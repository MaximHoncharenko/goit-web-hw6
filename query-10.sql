SELECT DISTINCT subjects.name AS subject_name
FROM grades
JOIN subjects ON grades.subject_id = subjects.id
JOIN students ON grades.student_id = students.id
JOIN teachers ON subjects.teacher_id = teachers.id
WHERE students.name = 'Desiree Robertson' 
AND teachers.name = 'Alexander Coleman';  