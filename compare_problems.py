import json

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 제1회 문제 목록
round1 = [q['number'] for q in data['questions'] if q['exam'] == '제1회']
round1_sorted = sorted(set(round1))

print("제1회 문제 번호:")
print(f"  {round1_sorted}")
print(f"\n개수: {len(round1_sorted)}개")

# docx에서 찾은 것
docx_round1 = [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 20, 22, 25, 28, 32, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 52, 53, 54, 55, 56, 58, 60]

print(f"\ndocx에서 찾은 제1회 문제 번호:")
print(f"  {docx_round1}")
print(f"  개수: {len(docx_round1)}개")

print("\ndocx에는 있는데 JSON에 없는 문제:")
missing = set(docx_round1) - set(round1_sorted)
print(f"  {sorted(missing) if missing else '없음'}")

print("\nJSON에 있는데 docx에서 못 찾은 문제:")
extra = set(round1_sorted) - set(docx_round1)
print(f"  {sorted(extra) if extra else '없음'}")
