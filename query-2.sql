SELECT students.name AS student_name, 
       AVG(grades.grade) AS average_grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE subjects.name = 'Math' 
GROUP BY students.id
ORDER BY average_grade DESC
LIMIT 1;