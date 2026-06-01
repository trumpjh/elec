import json

with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

nums = sorted([q['number'] for q in questions['questions']])
print(f"Total problems: {len(nums)}")
print(f"First 30: {nums[:30]}")
print(f"All numbers: {nums}")
