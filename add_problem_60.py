import json

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 문제 60 추가
problem_60 = {
    'number': 60,
    'question': '다음 보기 중 금속관, 애자, 합성수지관 및 케이블 공사가 모두 가능한 특수 장소를 옳게 나열한 것은',
    'options': ['화약고 등의 위험 장소', '목욕실', '부식성 가스가 나오는 장소', '습도가 높은 곳'],
    'answer': 3,
    'exam': '제1회'
}

# 제1회 마지막에 추가
data['questions'].append(problem_60)

# 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ 문제 60 추가됨")

# 확인
from collections import defaultdict
by_exam = defaultdict(list)
for q in data['questions']:
    by_exam[q['exam']].append(q['number'])

print("\n최종 회차별 문제 개수:")
for exam in sorted(by_exam.keys(), key=lambda x: int(x[1])):
    nums = sorted(by_exam[exam])
    print(f"  {exam}: {len(nums)}개")
    
print(f"\n✅ 총 {len(data['questions'])}개 문제")
