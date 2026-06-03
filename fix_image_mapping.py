import json
import re
import os

# 현재 JSON 읽기
with open('questions.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

# 이미지 파일 목록
image_dir = 'images'
image_files = sorted(os.listdir(image_dir)) if os.path.exists(image_dir) else []

print("=== 이미지 파일 목록 ===")
for i, f in enumerate(image_files, 1):
    print(f"{i}. {f}")

# 각 파일을 정확하게 파싱
print("\n=== 파일명 파싱 ===")
for filename in image_files:
    # 회차 추출
    exam_match = re.search(r'제(\d)회', filename)
    # 문제 번호 추출
    num_match = re.search(r'(\d+)번', filename)
    
    exam = exam_match.group(1) if exam_match else "?"
    num = num_match.group(1) if num_match else "?"
    
    # 문제/설명 구분
    img_type = "설명" if "설명" in filename else "문제"
    
    print(f"{filename}")
    print(f"  -> 제{exam}회 {num}번 ({img_type} 이미지)")

# 이제 JSON에 매핑
print("\n=== JSON 매핑 ===")

# 먼저 현재 매핑 상태 초기화 (image와 explanation_image 필드 초기화 또는 유지)
# 문제 이미지와 설명 이미지를 명확히 구분해서 매핑

for q in questions_data['questions']:
    exam_num = q['exam'].replace('제', '').replace('회', '')
    problem_num = q['number']
    
    # 각 이미지 파일과 매칭
    for filename in image_files:
        exam_match = re.search(r'제(\d)회', filename)
        num_match = re.search(r'(\d+)번', filename)
        
        if exam_match and num_match:
            file_exam = exam_match.group(1)
            file_num = num_match.group(1)
            
            # 회차와 번호가 일치하는 경우
            if file_exam == exam_num and file_num == str(problem_num):
                img_path = f'images/{filename}'
                
                if "설명" in filename:
                    q['explanation_image'] = img_path
                    print(f"문제 #{problem_num} (제{exam_num}회) 설명 이미지: {filename}")
                else:
                    q['image'] = img_path
                    print(f"문제 #{problem_num} (제{exam_num}회) 문제 이미지: {filename}")

# JSON 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions_data, f, ensure_ascii=False, indent=2)

print("\n✓ JSON 저장 완료")
