import json
from collections import defaultdict

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"총 문제 수: {data['total']}")

exams = defaultdict(list)
for q in data['questions']:
    exams[q['exam']].append(q['number'])

print("\n회차별 분포:")
total_q = 0
for exam in sorted(exams.keys()):
    unique_nums = sorted(set(exams[exam]))
    count = len(unique_nums)
    total_q += count
    print(f"  {exam}: {count}개 - {unique_nums}")

print(f"\n총합: {total_q}개")

# 선택지가 불완전한 문제
print("\n선택지 부족 문제:")
for q in data['questions']:
    if len(q['options']) < 4:
        print(f"  {q['exam']} 문제 {q['number']}: {len(q['options'])}개 옵션")
