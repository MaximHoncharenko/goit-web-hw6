SELECT groups.name AS group_name, 
       AVG(grades.grade) AS average_grade
FROM grades
JOIN students ON grades.student_id = students.id
JOIN groups ON students.group_id = groups.id
JOIN subjects ON grades.subject_id = subjects.id
WHERE subjects.name = 'Math'
GROUP BY groups.id
ORDER BY average_grade DESC;