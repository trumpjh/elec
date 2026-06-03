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

# 2. 현재 JSON 읽기
with open('questions.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

# 3. 이미지 파일 목록 - 전체 경로로
image_dir = 'images'
image_files = []
if os.path.exists(image_dir):
    for filename in os.listdir(image_dir):
        full_path = os.path.join(image_dir, filename)
        image_files.append((filename, full_path))

print(f"✓ 이미지 파일 {len(image_files)}개")

# 4. 이미지 파일 분류
problem_images = {}  # 문제 이미지: (exam, number) -> filename
explanation_images = {}  # 설명 이미지: (exam, number) -> filename

for filename, _ in image_files:
    # 문제 이미지인지 설명 이미지인지 확인
    is_problem_image = '문제' in filename and '설명' not in filename
    is_explanation_image = '설명' in filename
    
    # 정규식으로 회차와 문제 번호 추출
    # 형식: "제X회" "Y번"
    match = re.search(r'제(\d+)회[^\d]*(\d+)번', filename)
    if match:
        exam_num = int(match.group(1))
        problem_num = int(match.group(2))
        
        if is_problem_image:
            problem_images[(exam_num, problem_num)] = filename
            print(f"  문제 이미지: 제{exam_num}회 {problem_num}번 -> {filename}")
        elif is_explanation_image:
            explanation_images[(exam_num, problem_num)] = filename
            print(f"  설명 이미지: 제{exam_num}회 {problem_num}번 -> {filename}")

# 5. JSON에 이미지 매핑
updated_count = 0
explanation_count = 0

for q in questions_data['questions']:
    exam_num = int(q['exam'].replace('제', '').replace('회', ''))
    problem_num = q['number']
    
    # 설명 업데이트
    problem_idx = q['number'] - 1
    # 문제 숫자가 순차적이 아니므로, question 배열에서 찾아야 함
    # 다시 처리...
    
    # 실제로는 questions_data['questions'] 배열의 순서가 중요
    # 각 문제를 인덱스로 찾자
    
print("\n이미지 매핑 완료")
