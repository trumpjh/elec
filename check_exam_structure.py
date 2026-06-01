from docx import Document
import re

doc = Document('2025년도 문제.docx')

print("=" * 80)
print("회차별 문제 구조 파악")
print("=" * 80)

problems = []
current_exam = "회차 정보 없음"

for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    
    # 회차 표시 찾기
    if any(keyword in text for keyword in ['제1회', '제2회', '제3회', '회차']):
        exam_match = re.search(r'제(\d+)회', text)
        if exam_match:
            current_exam = f"제{exam_match.group(1)}회"
            print(f"\n{'='*60}")
            print(f"[{current_exam}] 시작 - 단락 {i}")
            print(f"{'='*60}")
    
    # 문제 패턴
    problem_match = re.match(r'^(\d+)\.\s+(.+)\?\s+([④③②①])\s*$', text)
    if problem_match:
        num = int(problem_match.group(1))
        q_text = problem_match.group(2)[:50]
        answer = problem_match.group(3)
        
        problems.append({
            'para': i,
            'number': num,
            'exam': current_exam,
            'question': q_text,
            'answer': answer
        })
        
        print(f"  문제 {num}: {q_text}... (정답: {answer})")

print("\n" + "=" * 80)
print("📊 최종 요약")
print("=" * 80)

# 회차별 그룹화
from collections import defaultdict
by_exam = defaultdict(list)

for p in problems:
    by_exam[p['exam']].append(p['number'])

print("\n회차별 문제 개수:")
for exam in sorted(by_exam.keys()):
    counts = by_exam[exam]
    print(f"  {exam}: {len(counts)}개 (번호: {min(counts)}~{max(counts)})")

print(f"\n총 추출 문제: {len(problems)}개")
print(f"문제 번호 범위: {min(p['number'] for p in problems)}~{max(p['number'] for p in problems)}")
