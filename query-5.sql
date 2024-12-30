SELECT subjects.name AS subject_name
FROM subjects
JOIN teachers ON subjects.teacher_id = teachers.id
WHERE teachers.name = 'Alexander Coleman';