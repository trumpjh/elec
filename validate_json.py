"""
questions.json 검증
"""
import json

try:
    data = json.load(open('questions.json', 'r', encoding='utf-8'))
    print(f'✓ JSON 형식 정상')
    print(f'  총 문제: {data["total"]}')
    print(f'  첫 번째 문제: {data["questions"][0]["number"]}')
    
    # 이미지 있는 문제 확인
    image_problems = [q for q in data['questions'] if q.get('image')]
    print(f'  이미지 있는 문제: {len(image_problems)}')
    
    for q in image_problems:
        print(f'    - {q["exam"]} 문제 {q["number"]}: {q["image"]}')
    
except json.JSONDecodeError as e:
    print(f'❌ JSON 형식 에러: {e}')
except Exception as e:
    print(f'❌ 에러: {e}')
