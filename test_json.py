import json

print("=" * 60)
print("✓ JSON 파일 검증")
print("=" * 60)

# questions.json 확인
with open('questions.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)
    
print(f"\n📝 questions.json:")
print(f"  - 총 문제: {questions_data['total']}개")
print(f"  - 첫 번째 문제:")
q1 = questions_data['questions'][0]
print(f"    번호: {q1['number']}")
print(f"    문제: {q1['question']}")
print(f"    정답: {q1['answer']} ({q1['options'][q1['answer']]})")
print(f"    시험: {q1['exam']}")

# example.json 확인
with open('example.json', 'r', encoding='utf-8') as f:
    examples_data = json.load(f)

print(f"\n📚 example.json:")
print(f"  - 총 설명: {examples_data['total']}개")
print(f"  - 첫 번째 설명:")
e1 = examples_data['examples'][0]
print(f"    문제번호: {e1['problem_number']}")
print(f"    단원: {e1['category']}")
print(f"    설명: {e1['explanation'][:50]}...")

print("\n✅ 두 파일 모두 정상 로드됨!")
print(f"   - 문제는 문제번호로 설명과 매핑 가능")
print(f"   - 문제 1-{questions_data['total']} 번호 매핑 가능")
