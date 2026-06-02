"""
제4회 문제 9의 전체 데이터 확인
"""
import json

data = json.load(open('questions.json', 'r', encoding='utf-8'))

for q in data['questions']:
    if q['exam'] == '제4회' and q['number'] == 9:
        print("【제4회 문제 9】")
        print("-" * 50)
        for key, value in q.items():
            if key == 'options':
                print(f"{key}:")
                for i, opt in enumerate(value):
                    print(f"  [{i}]: {opt}")
            else:
                value_str = str(value)[:60] if isinstance(value, str) else str(value)
                print(f"{key}: {value_str}")
        break
