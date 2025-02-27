import requests
import json
from datetime import date

# API基础URL
BASE_URL = 'http://localhost:8000/db'

def test_get_student_scores():
    """测试获取学生成绩接口"""
    print('\n测试获取学生成绩...')
    student_id = 1001  # 使用示例学生ID
    response = requests.get(f'{BASE_URL}/student/{student_id}/scores')
    
    if response.status_code == 200:
        scores = response.json()
        print(f'学生成绩获取成功，共{len(scores)}条记录：')
        for score in scores:
            print(f"学生：{score['student_name']}")
            print(f"课程：{score['course_name']}")
            print(f"分数：{score['score']}")
            print(f"考试日期：{score['exam_date']}\n")
    else:
        print(f'获取学生成绩失败：{response.json()["detail"]}')

def test_get_class_average_scores():
    """测试获取班级平均分接口"""
    print('\n测试获取班级平均分...')
    response = requests.get(f'{BASE_URL}/class/average-scores')
    
    if response.status_code == 200:
        averages = response.json()
        print('班级平均分获取成功：')
        for avg in averages:
            print(f"班级：{avg['class_name']}")
            print(f"课程：{avg['course_name']}")
            print(f"平均分：{avg['avg_score']}\n")
    else:
        print(f'获取班级平均分失败：{response.json()["detail"]}')

def test_get_course_top_students():
    """测试获取课程排名接口"""
    print('\n测试获取课程排名...')
    course_id = 1  # 使用示例课程ID
    limit = 3      # 获取前3名
    response = requests.get(f'{BASE_URL}/course/{course_id}/top-students?limit={limit}')
    
    if response.status_code == 200:
        rankings = response.json()
        print(f'课程排名获取成功，前{limit}名学生：')
        for rank in rankings:
            print(f"课程：{rank['course_name']}")
            print(f"学生：{rank['student_name']}")
            print(f"分数：{rank['score']}")
            print(f"排名：第{rank['rank']}名\n")
    else:
        print(f'获取课程排名失败：{response.json()["detail"]}')

def main():
    """运行所有测试"""
    print('开始测试学生成绩管理系统API...')
    
    try:
        # 测试获取学生成绩
        test_get_student_scores()
        
        # 测试获取班级平均分
        test_get_class_average_scores()
        
        # 测试获取课程排名
        test_get_course_top_students()
        
        print('所有测试完成！')
    except requests.exceptions.ConnectionError:
        print('错误：无法连接到服务器，请确保服务器已启动且地址正确。')
    except Exception as e:
        print(f'测试过程中出现错误：{str(e)}')

if __name__ == '__main__':
    main()