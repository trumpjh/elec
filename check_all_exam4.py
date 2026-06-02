import json

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 70)
print("제4회 모든 문제의 선택지 개수 확인")
print("=" * 70)

exam4_problems = [q for q in data['questions'] if q['exam'] == '제4회']

# 선택지 개수별로 정렬
problems_by_count = {}
for q in exam4_problems:
    count = len(q['options'])
    if count not in problems_by_count:
        problems_by_count[count] = []
    problems_by_count[count].append(q['number'])

# 결과 출력
for count in sorted(problems_by_count.keys()):
    print(f"\n선택지 {count}개: {len(problems_by_count[count])}개 문제")
    print(f"  문제 번호: {sorted(problems_by_count[count])}")
    
    if count < 4:
        print(f"  ⚠️  불완전한 문제들:")
        for q in exam4_problems:
            if q['number'] in problems_by_count[count]:
                print(f"    - {q['number']}번: {q['question'][:50]}...")
