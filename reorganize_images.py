"""
사용자의 이미지 파일을 정리하여 questions.json에 적용
"""
import json
import os
import shutil
from pathlib import Path

print("\n" + "="*70)
print("📁 이미지 파일 정리 및 적용")
print("="*70)

# 1단계: 이미지 파일 목록 수집 및 매핑
image_files = {
    ('제1회', 2): '2025년도 문제 제1회 2번.jpg',
    ('제2회', 2): '2025년도 문제  제2회 2번.png',  # 스페이스 주의
    ('제3회', 52): '2025년도 문제 제3회 52번.png',
    ('제3회', 59): '2025년도 문제 제3회 59번.png',
    ('제4회', 9): '2025년도 제4회 문제 9번.png',
}

print("\n【발견된 이미지 파일】")
print("-" * 70)

for (exam, num), filename in image_files.items():
    source_path = f"c:\\Users\\Administrator\\Documents\\history\\elec\\{filename}"
    if os.path.exists(source_path):
        print(f"✓ {exam} 문제 {num}: {filename}")
    else:
        print(f"❌ {exam} 문제 {num}: {filename} (파일 없음)")

# 2단계: images 폴더 정리
images_dir = "images"
if os.path.exists(images_dir):
    print(f"\n【기존 images 폴더 정리】")
    print("-" * 70)
    for file in os.listdir(images_dir):
        filepath = os.path.join(images_dir, file)
        if os.path.isfile(filepath):
            os.remove(filepath)
            print(f"  삭제: {file}")

# 3단계: 새 이미지 파일 이동
print(f"\n【이미지 파일 이동】")
print("-" * 70)

for (exam, num), filename in image_files.items():
    source = f"c:\\Users\\Administrator\\Documents\\history\\elec\\{filename}"
    
    if os.path.exists(source):
        # 파일 확장자 유지
        _, ext = os.path.splitext(filename)
        dest_filename = f"{exam}_{num}{ext}"
        dest = os.path.join(images_dir, dest_filename)
        
        shutil.copy(source, dest)
        print(f"✓ {filename} → {dest_filename}")

# 4단계: questions.json 업데이트
print(f"\n【questions.json 업데이트】")
print("-" * 70)

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 먼저 모든 image 필드 초기화
for q in data['questions']:
    q['image'] = None

# 새로운 이미지 매핑
for (exam, num), filename in image_files.items():
    source = f"c:\\Users\\Administrator\\Documents\\history\\elec\\{filename}"
    
    if os.path.exists(source):
        _, ext = os.path.splitext(filename)
        dest_filename = f"{exam}_{num}{ext}"
        
        for q in data['questions']:
            if q['exam'] == exam and q['number'] == num:
                q['image'] = f"images/{dest_filename}"
                print(f"✓ {exam} 문제 {num}: images/{dest_filename}")
                break

# 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✓ questions.json 저장 완료")

# 5단계: 최종 확인
print(f"\n【최종 상태】")
print("-" * 70)

problems_with_images = [q for q in data['questions'] if q.get('image')]
print(f"\n이미지 포함 문제: {len(problems_with_images)}개\n")

for q in sorted(problems_with_images, key=lambda x: (x['exam'], x['number'])):
    print(f"  {q['exam']} 문제 {q['number']}: {q['image']}")

print("\n" + "="*70)
print("✅ 이미지 파일 정리 완료!")
print("="*70)
