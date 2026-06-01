from docx import Document
import re

doc = Document('2025년도 문제.docx')

print("=" * 80)
print("모든 문단 출력 (문제 패턴 분석)")
print("=" * 80)

current_exam = ""
problem_count = 0
other_count = 0

for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    
    if not text:
        continue
    
    # 회차 표시
    exam_match = re.search(r'제(\d+)회', text)
    if exam_match:
        current_exam = f"제{exam_match.group(1)}회"
        print(f"\n{'='*70}")
        print(f"[{current_exam}] - 단락 {i}")
        print(f"{'='*70}")
        continue
    
    # 문제 패턴 (정규)
    normal_pattern = re.match(r'^(\d+)\.\s+(.+)\?\s+([④③②①])\s*$', text)
    if normal_pattern:
        problem_count += 1
        num = normal_pattern.group(1)
        q = normal_pattern.group(2)[:35]
        ans = normal_pattern.group(3)
        print(f"✓ 문제 {num}: {q}... (답: {ans})")
        continue
    
    # 다른 패턴의 문제들 확인
    if re.match(r'^\d+\.\s+', text):  # "번호." 로 시작
        other_count += 1
        print(f"? 다른형식: {text[:60]}...")

print(f"\n" + "=" * 80)
print(f"정규 문제: {problem_count}개")
print(f"다른 형식: {other_count}개")
print(f"총: {problem_count + other_count}개")
