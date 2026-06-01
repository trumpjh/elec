import json
from collections import defaultdict

# 기존 questions.json 로드
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 제1회 문제 13이 있는지 확인
has_problem_13 = any(q['number'] == 13 and q['exam'] == '제1회' for q in data['questions'])

print(f"제1회 문제 13 존재: {has_problem_13}")

if not has_problem_13:
    # 문제 13 추가
    problem_13 = {
        'number': 13,
        'question': '22.9[kV-Y] 가공전선의 굵기는 단면적이 몇 [mm²]이상이어야 하는가(단, 동선의 경우이다.)',
        'options': ['22', '32', '40', '50'],
        'answer': 0,
        'exam': '제1회'
    }
    
    # 제1회 문제 14 다음에 추가 (정렬)
    data['questions'].insert(8, problem_13)  # 14번 앞에 추가
    
    # 저장
    with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✓ 문제 13 추가됨")

# 최종 확인
by_exam = defaultdict(int)
for q in data['questions']:
    by_exam[q['exam']] += 1

print("\n회차별 최종 문제 개수:")
for exam in sorted(by_exam.keys(), key=lambda x: int(x[1])):
    print(f"  {exam}: {by_exam[exam]}개")

print(f"\n총: {len(data['questions'])}개")
