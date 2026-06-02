"""
제4회 문제 확인
"""
import json

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

exam4_problems = [q for q in data['questions'] if q['exam'] == '제4회']
print(f'\n제4회 문제 수: {len(exam4_problems)}\n')

for q in sorted(exam4_problems, key=lambda x: x['number']):
    image_info = f" [이미지: {q['image']}]" if q.get('image') else ""
    print(f"  문제 {q['number']}: {q['question'][:45]}...{image_info}")
