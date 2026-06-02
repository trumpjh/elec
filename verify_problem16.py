import json

data = json.load(open('questions.json', encoding='utf-8'))

# 제1회 16번 문제
q16 = [q for q in data['questions'] if q['exam']=='제1회' and q['number']==16]

if q16:
    q = q16[0]
    print("\n" + "="*70)
    print("✅ 제1회 16번 문제 확인")
    print("="*70)
    print(f"\n📝 문제: {q['question']}")
    print(f"\n📚 단원: {q['category']}")
    print(f"\n💡 설명:")
    print(f"   {q['explanation']}")
    print(f"\n✔ 정답: {['①', '②', '③', '④'][q['answer']]}")
    print(f"\n🔤 선택지 개수: {len(q['options'])}개")
else:
    print("❌ 제1회 16번 문제를 찾을 수 없습니다.")
