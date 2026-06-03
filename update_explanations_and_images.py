from docx import Document
import json
import re
import os

# 1. docx에서 모든 설명 추출
doc = Document('2025년도 설명.docx')
docx_explanations = []

for table in doc.tables:
    if len(table.rows) > 0:
        explanation_text = table.rows[0].cells[0].text.strip()
        docx_explanations.append(explanation_text)

print(f"✓ docx에서 {len(docx_explanations)}개 설명 추출")

# 2. 현재 JSON 읽기
with open('questions.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

print(f"✓ JSON에서 {len(questions_data['questions'])}개 문제 읽기")

# 3. 이미지 파일 목록
image_dir = 'images'
image_files = os.listdir(image_dir) if os.path.exists(image_dir) else []
print(f"✓ images 폴더에서 {len(image_files)}개 파일 확인")

# 4. 설명 업데이트 및 이미지 매핑
updated_count = 0
image_mapped_count = 0

for i, q in enumerate(questions_data['questions']):
    # 설명 업데이트
    if i < len(docx_explanations):
        docx_exp = docx_explanations[i]
        if q['explanation'] != docx_exp:
            q['explanation'] = docx_exp
            updated_count += 1
    
    # 이미지 파일과 매핑 (설명 이미지)
    # 파일명 형식: "2025년도 제N회 M번.ext" 또는 "2025년도 문제 제N회 M번.ext"
    problem_num = q['number']
    exam_num = int(q['exam'].replace('제', '').replace('회', ''))
    
    # 설명 이미지 찾기
    pattern = f'제{exam_num}회.*{problem_num}번'
    for img_file in image_files:
        if re.search(pattern, img_file):
            # 현재 "image" 필드에 이미지가 있는지 확인
            if 'image' not in q or not q['image']:
                # image가 없으면 explanation_image에 할당
                q['explanation_image'] = f'images/{img_file}'
                image_mapped_count += 1
            else:
                # image가 이미 있으면 explanation_image에 할당
                if 'explanation_image' not in q or q['explanation_image'] != f'images/{img_file}':
                    q['explanation_image'] = f'images/{img_file}'
                    image_mapped_count += 1
            break

# 5. 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions_data, f, ensure_ascii=False, indent=2)

print(f"\n✓ 설명 업데이트: {updated_count}개")
print(f"✓ 이미지 매핑: {image_mapped_count}개")
print(f"✓ JSON 저장 완료")
