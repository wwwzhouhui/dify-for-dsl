-- 创建学生表
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(50) NOT NULL,
    gender CHAR(1),
    class_name VARCHAR(20),
    admission_date DATE
);

-- 创建课程表
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    credit DECIMAL(3,1)
);

-- 创建成绩表
CREATE TABLE scores (
    score_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    score DECIMAL(5,2),
    exam_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- 插入测试数据
-- 1. 插入学生数据
INSERT INTO students (student_id, student_name, gender, class_name, admission_date) VALUES
(1001, '张三', 'M', '高一(1)班', '2023-09-01'),
(1002, '李四', 'F', '高一(1)班', '2023-09-01'),
(1003, '王五', 'M', '高一(2)班', '2023-09-01'),
(1004, '赵六', 'F', '高一(2)班', '2023-09-01'),
(1005, '孙七', 'M', '高一(3)班', '2023-09-01');

-- 2. 插入课程数据
INSERT INTO courses (course_id, course_name, credit) VALUES
(1, '语文', 4.0),
(2, '数学', 4.0),
(3, '英语', 4.0),
(4, '物理', 3.0),
(5, '化学', 3.0);

-- 3. 插入成绩数据
INSERT INTO scores (score_id, student_id, course_id, score, exam_date) VALUES
(1, 1001, 1, 85.5, '2023-12-20'),
(2, 1001, 2, 92.0, '2023-12-20'),
(3, 1001, 3, 78.5, '2023-12-20'),
(4, 1002, 1, 88.0, '2023-12-20'),
(5, 1002, 2, 95.5, '2023-12-20'),
(6, 1002, 3, 90.0, '2023-12-20'),
(7, 1003, 1, 82.5, '2023-12-20'),
(8, 1003, 2, 86.0, '2023-12-20'),
(9, 1003, 3, 75.5, '2023-12-20'),
(10, 1004, 1, 91.0, '2023-12-20'),
(11, 1004, 2, 89.5, '2023-12-20'),
(12, 1004, 3, 94.0, '2023-12-20'),
(13, 1005, 1, 87.5, '2023-12-20'),
(14, 1005, 2, 88.0, '2023-12-20'),
(15, 1005, 3, 85.5, '2023-12-20');

-- 一些常用查询示例
-- 1. 查询某个学生的所有成绩
SELECT s.student_name, c.course_name, sc.score
FROM students s
JOIN scores sc ON s.student_id = sc.student_id
JOIN courses c ON sc.course_id = c.course_id
WHERE s.student_id = 1001;

-- 2. 查询某个班级的平均成绩
SELECT s.class_name, c.course_name, AVG(sc.score) as avg_score
FROM students s
JOIN scores sc ON s.student_id = sc.student_id
JOIN courses c ON sc.course_id = c.course_id
GROUP BY s.class_name, c.course_name;

-- 3. 查询各科成绩排名前三的学生
WITH RankedScores AS (
    SELECT 
        c.course_name,
        s.student_name,
        sc.score,
        RANK() OVER (PARTITION BY c.course_id ORDER BY sc.score DESC) as student_rank
    FROM scores sc
    JOIN students s ON sc.student_id = s.student_id
    JOIN courses c ON sc.course_id = c.course_id
)
SELECT * FROM RankedScores WHERE student_rank <= 3;