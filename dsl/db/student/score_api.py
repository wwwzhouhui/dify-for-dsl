from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database import get_db
from models import Student, Course, Score
from pydantic import BaseModel
from datetime import date

app = FastAPI(
    title="学生成绩管理系统API",
    description="提供学生成绩查询、统计分析等功能",
    version="1.0.0"
)

class ScoreResponse(BaseModel):
    student_name: str
    course_name: str
    score: float
    exam_date: date

    class Config:
        orm_mode = True

class ClassAvgResponse(BaseModel):
    class_name: str
    course_name: str
    avg_score: float

    class Config:
        orm_mode = True

class RankResponse(BaseModel):
    course_name: str
    student_name: str
    score: float
    rank: int

    class Config:
        orm_mode = True

@app.get("/db/student/{student_id}/scores", response_model=List[ScoreResponse])
async def get_student_scores(student_id: int, db: Session = Depends(get_db)):
    """获取指定学生的所有成绩"""
    scores = db.query(Score, Student, Course)\
        .join(Student, Score.student_id == Student.student_id)\
        .join(Course, Score.course_id == Course.course_id)\
        .filter(Student.student_id == student_id)\
        .all()
    
    if not scores:
        raise HTTPException(status_code=404, detail="未找到该学生的成绩记录")
    
    return [
        ScoreResponse(
            student_name=score[1].student_name,
            course_name=score[2].course_name,
            score=score[0].score,
            exam_date=score[0].exam_date
        ) for score in scores
    ]

@app.get("/db/class/average-scores", response_model=List[ClassAvgResponse])
async def get_class_average_scores(db: Session = Depends(get_db)):
    """获取各个班级的平均成绩"""
    class_averages = db.query(
        Student.class_name,
        Course.course_name,
        func.avg(Score.score).label('avg_score')
    ).join(Score, Student.student_id == Score.student_id)\
    .join(Course, Score.course_id == Course.course_id)\
    .group_by(Student.class_name, Course.course_name)\
    .all()
    
    return [
        ClassAvgResponse(
            class_name=avg[0],
            course_name=avg[1],
            avg_score=round(float(avg[2]), 2)
        ) for avg in class_averages
    ]

@app.get( "/db/course/{course_id}/top-students", response_model=List[RankResponse])
async def get_course_top_students(course_id: int, limit: int = 3, db: Session = Depends(get_db)):
    """获取指定课程成绩排名前N的学生"""
    from sqlalchemy import text
    
    query = text("""
        WITH RankedScores AS (
            SELECT 
                c.course_name,
                s.student_name,
                sc.score,
                RANK() OVER (PARTITION BY c.course_id ORDER BY sc.score DESC) as student_rank
            FROM scores sc
            JOIN students s ON sc.student_id = s.student_id
            JOIN courses c ON sc.course_id = c.course_id
            WHERE c.course_id = :course_id
        )
        SELECT * FROM RankedScores WHERE student_rank <= :limit
    """)
    
    results = db.execute(query, {"course_id": course_id, "limit": limit}).fetchall()
    
    if not results:
        raise HTTPException(status_code=404, detail="未找到该课程的成绩记录")
    
    return [
        RankResponse(
            course_name=result[0],
            student_name=result[1],
            score=float(result[2]),
            rank=result[3]
        ) for result in results
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)