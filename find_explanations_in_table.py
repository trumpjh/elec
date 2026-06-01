from docx import Document
import json
import re

doc = Document('2025년도 문제.docx')

# 모든 테이블 순회
all_explanations = {}

for table_idx, table in enumerate(doc.tables):
    for row in table.rows:
        cells = row.cells
        if len(cells) >= 2:
            first_cell = cells[0].text.strip()
            second_cell = cells[1].text.strip()
            
            # 문제 번호 추출
            match = re.match(r'^(\d+)\s*\.', first_cell)
            if match:
                problem_num = int(match.group(1))
                explanation = second_cell[:500]  # 첫 500자
                all_explanations[problem_num] = explanation

print("=" * 80)
print("테이블에서 추출된 모든 문제 번호:")
print("=" * 80)

# 그룹화
round1 = [k for k in sorted(all_explanations.keys()) if k <= 32]
round2 = [k for k in sorted(all_explanations.keys()) if 32 < k <= 48]
round3 = [k for k in sorted(all_explanations.keys()) if 48 < k <= 60]
round4 = [k for k in sorted(all_explanations.keys()) if k > 60]

print(f"\n제1회 (1-32): {round1}")
print(f"제2회 (33-48): {round2}")
print(f"제3회 (49-60): {round3}")
print(f"제4회 (61-75): {round4}")

# 누락 확인
missing = [39, 60, 8]  # 실제 문제 번호
print("\n" + "=" * 80)
print("누락된 설명 찾기:")
print("=" * 80)

for num in missing:
    if num in all_explanations:
        print(f"\n✓ 문제 {num}: {all_explanations[num][:200]}")
    else:
        print(f"\n✗ 문제 {num}: 테이블에서 미발견")
