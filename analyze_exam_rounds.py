from docx import Document
import re

doc = Document('2025년도 문제.docx')

print("=" * 80)
print("문제 구조 상세 분석 - 회차별 분석")
print("=" * 80)

problems = []
current_exam = ""

for para in doc.paragraphs:
    text = para.text.strip()
    
    # 회차 표시 찾기 (제1회, 제2회 등)
    if '회차' in text or '제' in text and '회' in text:
        if '제' in text:
            # 예: "제1회 기출문제" 또는 "2025년도 제1회"
            exam_match = re.search(r'제(\d+)회', text)
            if exam_match:
                current_exam = f"제{exam_match.group(1)}회"
                print(f"\n🔹 [{current_exam}]", flush=True)
    
    # 문제 패턴: "1. 문제? ④"
    problem_match = re.match(r'^(\d+)\.\s+(.+)\?\s+([④③②①])\s*$', text)
    if problem_match:
        num = int(problem_match.group(1))
        question_text = problem_match.group(2)[:40]
        answer = problem_match.group(3)
        
        problems.append({
            'number': num,
            'exam': current_exam,
            'text': question_text,
            'answer': answer
        })
        
        # 문제 번호 1, 2, 3, 14 등만 상세 출력
        if num in [1, 2, 3, 14]:
            print(f"   {num}. {question_text}... (답: {answer})")

print("\n" + "=" * 80)
print("📊 요약")
print("=" * 80)

# 회차별 정리
by_exam = {}
by_number = {}

for p in problems:
    exam = p['exam'] or "회차 정보 없음"
    by_exam[exam] = by_exam.get(exam, 0) + 1
    
    key = (p['number'], exam)
    by_number[key] = by_number.get(key, 0) + 1

print("\n회차별 문제 개수:")
for exam, count in sorted(by_exam.items()):
    print(f"  {exam}: {count}개")

print(f"\n총 문제: {len(problems)}개")
print(f"고유 번호: {len(set(p['number'] for p in problems))}개")

# 중복 확인
print("\n중복된 문제 번호:")
duplicates = {}
for p in problems:
    duplicates[p['number']] = duplicates.get(p['number'], 0) + 1

for num in sorted(duplicates.keys()):
    if duplicates[num] > 1:
        print(f"  문제 {num}: {duplicates[num]}번 반복")
        # 해당 번호의 모든 정보 출력
        for p in problems:
            if p['number'] == num:
                print(f"     - {p['exam']}: {p['text'][:30]}...")
