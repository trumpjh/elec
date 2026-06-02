import json

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("제1회, 제2회, 제3회 문제 선택지 완전성 확인")
print("=" * 80)

exams = ['제1회', '제2회', '제3회']

for exam in exams:
    exam_problems = [q for q in data['questions'] if q['exam'] == exam]
    
    print(f"\n【{exam}】(총 {len(exam_problems)}개 문제)")
    print("-" * 80)
    
    # 선택지 개수별로 정렬
    problems_by_count = {}
    for q in exam_problems:
        count = len(q['options'])
        if count not in problems_by_count:
            problems_by_count[count] = []
        problems_by_count[count].append(q)
    
    # 결과 출력
    for count in sorted(problems_by_count.keys()):
        problems = problems_by_count[count]
        problem_nums = [str(p['number']) for p in sorted(problems, key=lambda x: x['number'])]
        
        if count == 4:
            print(f"✅ 선택지 4개: {len(problems)}개 문제")
            print(f"   문제 번호: {', '.join(problem_nums)}")
        else:
            print(f"⚠️  선택지 {count}개: {len(problems)}개 문제 (불완전)")
            print(f"   문제 번호: {', '.join(problem_nums)}")
            print(f"   상세:")
            for p in sorted(problems, key=lambda x: x['number']):
                print(f"     - {p['number']}번: {p['question'][:50]}...")
                print(f"       현재 선택지: {p['options']}")

print("\n" + "=" * 80)
print("요약")
print("=" * 80)

for exam in exams:
    exam_problems = [q for q in data['questions'] if q['exam'] == exam]
    incomplete = [q for q in exam_problems if len(q['options']) < 4]
    
    if incomplete:
        print(f"⚠️  {exam}: {len(incomplete)}개 문제 불완전")
        print(f"   {', '.join([str(p['number']) for p in incomplete])}번")
    else:
        print(f"✅ {exam}: 모든 문제 완전 (4개 선택지)")
