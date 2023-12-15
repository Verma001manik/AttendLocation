-- schema.sql
DROP TABLE IF EXISTS Attendance;
DROP TABLE IF EXISTS Students;

CREATE TABLE Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_rollno TEXT NOT NULL,
    student_name TEXT, 
    student_attendance_id INTEGER NOT NULL, 
    is_logged_in INTEGER DEFAULT 0,
    attendance_attempts INTEGER DEFAULT 2
);

CREATE TABLE Attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    student_id INTEGER,
    student_rollno TEXT NOT NULL,
    student_name TEXT, 
    date TEXT NOT NULL, 
    time TEXT NOT NULL, 
    status TEXT
);
