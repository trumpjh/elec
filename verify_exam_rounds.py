from docx import Document
import re
from collections import defaultdict

doc = Document('2025년도 문제.docx')

print("=" * 80)
print("회차별 문제 정확한 재분석")
print("=" * 80)

problems = []
current_exam = ""
current_exam_num = 0

# 모든 문제 추출
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    
    # 회차 표시 찾기
    exam_match = re.search(r'제(\d+)회', text)
    if exam_match:
        current_exam_num = int(exam_match.group(1))
        current_exam = f"제{current_exam_num}회"
        print(f"\n📍 [{current_exam}] 시작")
    
    # 문제 패턴
    problem_match = re.match(r'^(\d+)\.\s+(.+)\?\s+([④③②①])\s*$', text)
    if problem_match:
        num = int(problem_match.group(1))
        q_text = problem_match.group(2)[:40]
        
        problems.append({
            'number': num,
            'exam': current_exam,
            'exam_num': current_exam_num,
            'text': q_text
        })

# 회차별 그룹화
by_exam = defaultdict(list)
for p in problems:
    by_exam[p['exam']].append(p['number'])

print("\n" + "=" * 80)
print("📊 현재 추출 결과")
print("=" * 80)

total = 0
for exam in sorted(by_exam.keys(), key=lambda x: int(x[1])):
    count = len(by_exam[exam])
    total += count
    print(f"  {exam}: {count}개 (번호: {min(by_exam[exam])}~{max(by_exam[exam])})")

print(f"\n총 문제: {total}개")

print("\n" + "=" * 80)
print("예상 정보 (사용자 제시)")
print("=" * 80)
expected = {
    "제1회": 32,
    "제2회": 16,
    "제3회": 12,
    "제4회": 15
}

for exam, expected_count in expected.items():
    actual_count = len(by_exam.get(exam, []))
    status = "✓" if actual_count == expected_count else "✗"
    print(f"  {status} {exam}: 예상 {expected_count}개, 현재 {actual_count}개")

print(f"\n총 예상: {sum(expected.values())}개, 현재: {total}개")

# 중복 문제 번호 찾기
print("\n" + "=" * 80)
print("중복된 문제 번호 (같은 회차 내)")
print("=" * 80)

for exam in sorted(by_exam.keys(), key=lambda x: int(x[1])):
    numbers = by_exam[exam]
    duplicates = defaultdict(int)
    for n in numbers:
        duplicates[n] += 1
    
    has_dup = any(c > 1 for c in duplicates.values())
    if has_dup:
        print(f"\n{exam}:")
        for num, count in sorted(duplicates.items()):
            if count > 1:
                print(f"   문제 {num}: {count}번")
