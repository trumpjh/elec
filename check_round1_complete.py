from docx import Document
import re
from collections import defaultdict

doc = Document('2025년도 문제.docx')

# 제1회만 모든 문제 찾기 (정규식과 다른 형식 모두)
problems_round1 = []
current_exam = ""

for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    
    if not text:
        continue
    
    # 회차 표시
    exam_match = re.search(r'제(\d+)회', text)
    if exam_match:
        exam_num = int(exam_match.group(1))
        current_exam = f"제{exam_num}회"
        if exam_num > 1:
            break  # 제1회만 찾기
        continue
    
    if current_exam != "제1회":
        continue
    
    # 모든 문제 찾기 (어떤 형식이든)
    if re.match(r'^\d+\.\s+', text):
        # 정규 형식 확인
        match_regular = re.match(r'^(\d+)\.\s+(.+)\?\s+([④③②①])\s*$', text)
        if match_regular:
            num = int(match_regular.group(1))
            problems_round1.append({
                'number': num,
                'type': '정규',
                'text': text[:60]
            })
        else:
            # 다른 형식
            match_other = re.match(r'^(\d+)\.\s+(.+)\??\s*$', text)
            if match_other:
                num = int(match_other.group(1))
                problems_round1.append({
                    'number': num,
                    'type': '비정규',
                    'text': text[:60]
                })

# 정렬하고 출력
problems_round1.sort(key=lambda x: x['number'])

print("="*70)
print("제1회 모든 문제")
print("="*70)

for p in problems_round1:
    print(f"  {p['type']:5} | 문제 {p['number']:2}: {p['text']}")

print(f"\n총: {len(problems_round1)}개")

# 번호별 확인
nums = [p['number'] for p in problems_round1]
print(f"\n문제 번호: {min(nums)} ~ {max(nums)}")
print(f"고유 번호: {len(set(nums))}개")

# 누락된 번호 찾기
all_nums = set(range(1, 70))
found_nums = set(nums)
missing = sorted(all_nums - found_nums)

if missing:
    print(f"\n1~60 범위에서 누락된 번호:")
    print(f"  {missing}")
