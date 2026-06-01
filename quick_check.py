import json
from collections import defaultdict

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

by_exam = defaultdict(int)
for q in data['questions']:
    by_exam[q['exam']] += 1

print("회차별 문제 개수:")
for exam in sorted(by_exam.keys(), key=lambda x: int(x[1]) if x[1].isdigit() else 0):
    print(f"  {exam}: {by_exam[exam]}개")

print(f"\n총: {data['total']}개")
