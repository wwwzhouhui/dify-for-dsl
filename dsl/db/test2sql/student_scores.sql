-- 创建学生成绩表
CREATE TABLE `student_scores` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `student_id` varchar(20) NOT NULL COMMENT '学号',
  `student_name` varchar(50) NOT NULL COMMENT '学生姓名',
  `class_name` varchar(50) NOT NULL COMMENT '班级名称',
  `subject` varchar(50) NOT NULL COMMENT '科目名称',
  `score` decimal(5,2) NOT NULL COMMENT '分数',
  `exam_date` date NOT NULL COMMENT '考试日期',
  `semester` varchar(20) NOT NULL COMMENT '学期',
  `grade` varchar(20) NOT NULL COMMENT '年级',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_student_id` (`student_id`),
  KEY `idx_exam_date` (`exam_date`),
  KEY `idx_subject` (`subject`),
  KEY `idx_class` (`class_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生成绩信息表';

-- 清空并重置表
TRUNCATE TABLE student_scores;

-- 插入基础测试数据
INSERT INTO student_scores (student_id, student_name, class_name, subject, score, exam_date, semester, grade) 
WITH RECURSIVE numbers AS (
    SELECT 1 AS n UNION ALL SELECT n + 1 FROM numbers WHERE n < 100
),
random_data AS (
    SELECT 
        n,
        CONCAT('2023', LPAD(FLOOR(RAND() * 100), 3, '0')) as student_id,
        ELT(FLOOR(RAND() * 10) + 1, '张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十', '郑十一', '王十二') as student_name,
        ELT(FLOOR(RAND() * 4) + 1, '高一(1)班', '高一(2)班', '高一(3)班', '高一(4)班') as class_name,
        ELT(FLOOR(RAND() * 5) + 1, '语文', '数学', '英语', '物理', '化学') as subject,
        ROUND(60 + RAND() * 40, 2) as score,
        DATE_ADD('2023-12-01', INTERVAL FLOOR(RAND() * 30) DAY) as exam_date,
        '2023-2024学年第一学期' as semester,
        '高一' as grade
    FROM numbers
)
SELECT 
    student_id,
    student_name,
    class_name,
    subject,
    score,
    exam_date,
    semester,
    grade
FROM random_data;

-- 插入不及格成绩数据
INSERT INTO student_scores (student_id, student_name, class_name, subject, score, exam_date, semester, grade)
SELECT 
    CONCAT('2023', LPAD(FLOOR(RAND() * 100), 3, '0')),
    ELT(FLOOR(RAND() * 10) + 1, '张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十', '郑十一', '王十二'),
    ELT(FLOOR(RAND() * 4) + 1, '高一(1)班', '高一(2)班', '高一(3)班', '高一(4)班'),
    ELT(FLOOR(RAND() * 5) + 1, '语文', '数学', '英语', '物理', '化学'),
    ROUND(40 + RAND() * 19, 2),
    DATE_ADD('2023-12-01', INTERVAL FLOOR(RAND() * 30) DAY),
    '2023-2024学年第一学期',
    '高一'
FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) n;

-- 插入优秀成绩数据
INSERT INTO student_scores (student_id, student_name, class_name, subject, score, exam_date, semester, grade)
SELECT 
    CONCAT('2023', LPAD(FLOOR(RAND() * 100), 3, '0')),
    ELT(FLOOR(RAND() * 10) + 1, '张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十', '郑十一', '王十二'),
    ELT(FLOOR(RAND() * 4) + 1, '高一(1)班', '高一(2)班', '高一(3)班', '高一(4)班'),
    ELT(FLOOR(RAND() * 5) + 1, '语文', '数学', '英语', '物理', '化学'),
    ROUND(90 + RAND() * 10, 2),
    DATE_ADD('2023-12-01', INTERVAL FLOOR(RAND() * 30) DAY),
    '2023-2024学年第一学期',
    '高一'
FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) n;