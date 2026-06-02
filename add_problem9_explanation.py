"""
테이블 64의 전체 내용 확인 및 제4회 문제 9 설명 추가
"""
from docx import Document
import json

print("\n" + "="*70)
print("테이블 64 내용 및 제4회 문제 9 설명 추가")
print("="*70)

doc = Document('2025년도 설명.docx')

# 테이블 64 확인
table64 = doc.tables[64]

print("\n【테이블 64 전체 내용】")
print("-" * 70)

for row_idx, row in enumerate(table64.rows):
    for col_idx, cell in enumerate(row.cells):
        text = cell.text.strip()
        if text:
            print(f"행 {row_idx}, 열 {col_idx}: {text[:80]}...")

# 트라이액 설명 찾기
print("\n【트라이액 관련 내용 추출】")
print("-" * 70)

thyristor_explanation = ""
for row in table64.rows:
    for cell in row.cells:
        if '트라이액' in cell.text:
            print(f"찾음: {cell.text}")
            thyristor_explanation = cell.text

# 제4회 문제 9의 설명을 위해 새로운 설명 작성
problem9_explanation = """설명: 전기기기-반도체
- 트라이액(Thyristor): SCR(실리콘 제어정류기)와 유사한 4층 반도체 소자로, 게이트 신호에 의해 on/off 제어 가능
- 위상제어 회로: 교류 전원의 위상을 제어하여 전압이나 전류를 조절하는 회로
- 트라이액의 특징:
  * 역병렬 쌍의 SCR로 구성되어 양쪽 반주기 모두 제어 가능
  * 교류 전원에서 효율적인 전압 제어 가능
  * 모터 속도 제어, 히터 온도 제어 등에 사용"""

# questions.json 업데이트
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 제4회 문제 9 찾기
for q in data['questions']:
    if q['exam'] == '제4회' and q['number'] == 9:
        q['explanation'] = problem9_explanation
        q['category'] = '전기기기'
        print(f"\n✓ 제4회 문제 9 업데이트")
        print(f"  설명: {problem9_explanation[:50]}...")
        print(f"  카테고리: 전기기기")
        break

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✓ questions.json 저장 완료")

# 확인
print("\n【최종 이미지 포함 문제 목록】")
print("-" * 70)

problems_with_images = [q for q in data['questions'] if q.get('image')]
for q in sorted(problems_with_images, key=lambda x: (x['exam'], x['number'])):
    cat = f" | {q['category']}" if q.get('category') else ""
    img = f" | 이미지: {q.get('image', '')}" if q.get('image') else ""
    print(f"{q['exam']} 문제 {q['number']}{cat}{img}")

print("\n" + "="*70)
