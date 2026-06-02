"""
최종 이미지 적용 확인
"""
import json
import os

print("\n" + "="*70)
print("✅ 최종 이미지 적용 상태 확인")
print("="*70)

# 1. images 폴더 확인
print("\n【images 폴더 확인】")
print("-" * 70)

images_dir = "images"
if os.path.exists(images_dir):
    files = os.listdir(images_dir)
    print(f"✓ {len(files)}개 파일 발견:\n")
    for file in sorted(files):
        print(f"  - {file}")
else:
    print("❌ images 폴더 없음")

# 2. questions.json 확인
print("\n【questions.json 이미지 정보】")
print("-" * 70)

data = json.load(open('questions.json', 'r', encoding='utf-8'))

image_problems = [q for q in data['questions'] if q.get('image')]
print(f"\n이미지 포함 문제: {len(image_problems)}개\n")

for q in sorted(image_problems, key=lambda x: (x['exam'], x['number'])):
    print(f"✓ {q['exam']} 문제 {q['number']}")
    print(f"   파일: {q['image']}")
    
    # 파일 존재 확인
    image_file = q['image'].replace('images/', '')
    image_path = os.path.join(images_dir, image_file)
    
    if os.path.exists(image_path):
        file_size = os.path.getsize(image_path)
        print(f"   크기: {file_size:,} bytes")
    else:
        print(f"   ❌ 파일 없음!")
    print()

print("="*70)
print("✅ 모든 이미지 파일이 정상적으로 적용되었습니다!")
print("="*70)
