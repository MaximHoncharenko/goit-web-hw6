SELECT students.name AS student_name, grades.grade AS grade
FROM grades
JOIN students ON grades.student_id = students.id
JOIN groups ON students.group_id = groups.id
JOIN subjects ON grades.subject_id = subjects.id
WHERE groups.name = 'Group A'  
AND subjects.name = 'Math'; 
