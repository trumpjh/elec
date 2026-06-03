import json

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
# 제4회 문제 9번 찾기
found = False
for q in data['questions']:
    if q['exam'] == '제4회' and q['number'] == 9:
        print(f"Found: 문제 {q['number']} - {q['question'][:50]}...")
        print(f"Image: {q.get('image')}")
        found = True
        break

if not found:
    print("제4회 문제 9번을 찾을 수 없습니다")
    
# 제4회 모든 문제 번호 확인
print("\n제4회 문제 번호 목록:")
exam4_numbers = sorted(set(q['number'] for q in data['questions'] if q['exam'] == '제4회'))
print(exam4_numbers)
