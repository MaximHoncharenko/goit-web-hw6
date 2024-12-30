import sqlite3
from faker import Faker
import random

# Ініціалізація Faker
fake = Faker()

# Використання контекстного менеджера для роботи з базою даних
with sqlite3.connect("university.db") as connection:
    cursor = connection.cursor()

    # Створення таблиць
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        group_id INTEGER NOT NULL,
        FOREIGN KEY (group_id) REFERENCES groups(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        teacher_id INTEGER NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        grade INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
    );
    """)

    # Заповнення таблиць випадковими даними
    # Додавання груп
    groups = ["Group A", "Group B", "Group C"]
    for group in groups:
        cursor.execute("SELECT 1 FROM groups WHERE name = ?", (group,))
        if cursor.fetchone() is None:  # Перевірка наявності групи
            cursor.execute("INSERT INTO groups (name) VALUES (?)", (group,))

    # Додавання викладачів
    teachers = [fake.name() for _ in range(random.randint(3, 5))]
    for teacher in teachers:
        cursor.execute("SELECT 1 FROM teachers WHERE name = ?", (teacher,))
        if cursor.fetchone() is None:  # Перевірка наявності викладача
            cursor.execute("INSERT INTO teachers (name) VALUES (?)", (teacher,))

    # Додавання предметів
    subjects = ["Math", "Physics", "Chemistry", "History", "Biology", "Programming"]
    subject_teacher_map = {}
    for subject in subjects:
        cursor.execute("SELECT 1 FROM subjects WHERE name = ?", (subject,))
        if cursor.fetchone() is None:  # Перевірка наявності предмета
            teacher_id = random.randint(1, len(teachers))
            subject_teacher_map[subject] = teacher_id
            cursor.execute("INSERT INTO subjects (name, teacher_id) VALUES (?, ?)", (subject, teacher_id))

    # Додавання студентів
    group_ids = [row[0] for row in cursor.execute("SELECT id FROM groups").fetchall()]
    students_per_group = 50 // len(groups)  # Поділити 50 студентів на 3 групи

    for group_id in group_ids:
        for _ in range(students_per_group):
            name = fake.name()
            cursor.execute("SELECT 1 FROM students WHERE name = ? AND group_id = ?", (name, group_id))
            if cursor.fetchone() is None:  # Перевірка наявність студента
                cursor.execute("INSERT INTO students (name, group_id) VALUES (?, ?)", (name, group_id))

    # Додавання оцінок студентів (обмежуємо кількість оцінок до 3 для кожного предмета)
    student_ids = [row[0] for row in cursor.execute("SELECT id FROM students").fetchall()]
    subject_ids = [row[0] for row in cursor.execute("SELECT id FROM subjects").fetchall()]
    
    for student_id in student_ids:
        for subject_id in subject_ids:
            for _ in range(3):  # Генеруємо лише 3 оцінки на кожен предмет
                grade = random.randint(1, 100)
                date = fake.date_this_year().isoformat()
                cursor.execute("SELECT 1 FROM grades WHERE student_id = ? AND subject_id = ? AND grade = ? AND date = ?",
                               (student_id, subject_id, grade, date))
                if cursor.fetchone() is None:  # Перевірка наявність оцінки
                    cursor.execute("INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)",
                                   (student_id, subject_id, grade, date))

    # Збереження змін
    connection.commit()

print("База даних успішно створена та заповнена випадковими даними.")
