import json

# JSON 파일 로드
with open('questions.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

with open('example.json', 'r', encoding='utf-8') as f:
    examples_data = json.load(f)

# 문제와 설명 매핑
questions = questions_data['questions']
examples = examples_data['examples']

# 각 회차별 분석
exams = {}
for q in questions:
    exam = q['exam']
    if exam not in exams:
        exams[exam] = {'questions': [], 'found_explanation': 0}
    exams[exam]['questions'].append(q['number'])

example_problems = {e['problem_number']: e for e in examples}

# 회차별 상세 분석
print("=" * 80)
print("회차별 문제와 설명 일치도 분석")
print("=" * 80)

total_problems = 0
total_explanations = 0
missing_count = 0

for exam in sorted(exams.keys()):
    problems = sorted(exams[exam]['questions'])
    found = sum(1 for p in problems if p in example_problems)
    missing = [p for p in problems if p not in example_problems]
    
    exams[exam]['found_explanation'] = found
    total_problems += len(problems)
    total_explanations += found
    missing_count += len(missing)
    
    print(f"\n{exam}:")
    print(f"  전체 문제: {len(problems)}개")
    print(f"  설명 있는 문제: {found}개")
    print(f"  설명 없는 문제: {len(missing)}개")
    if missing:
        print(f"  설명 누락 문제 번호: {missing}")

print("\n" + "=" * 80)
print(f"전체 요약:")
print(f"  총 문제 개수: {total_problems}개")
print(f"  설명이 있는 문제: {total_explanations}개")
print(f"  설명이 없는 문제: {missing_count}개 ({(missing_count/total_problems*100):.1f}%)")
print("=" * 80)

# 설명에만 있는 문제 확인
example_only = [e['problem_number'] for e in examples if e['problem_number'] not in [q['number'] for q in questions]]
if example_only:
    print(f"\n⚠️ 설명에만 있는 문제 번호 (문제 없음): {example_only}")
