from docx import Document
import re

doc = Document('2025년도 설명.docx')

# 제1회 44번 주변의 이미지와 요소들을 추적
current_exam = None
element_list = list(doc.element.body)
image_count_in_doc = 0

for i, element in enumerate(element_list):
    if element.tag.endswith('p'):
        text = ''.join([t.text for t in element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
        
        if '2025년도' in text and '설명' in text:
            match = re.search(r'제(\d)회', text)
            if match:
                current_exam = int(match.group(1))
        
        if text and re.match(r'^\d+\.$', text.strip()):
            problem_num = int(text.strip()[:-1])
            if problem_num == 44:
                print(f"제{current_exam}회 44번 (인덱스 {i})")
    
    # 이미지 찾기
    if element.tag.endswith('p'):
        # 문단 내의 그리기/이미지 찾기
        drawings = element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing')
        if drawings:
            print(f"  [{i}] 문단에 이미지 발견 (총 {len(drawings)}개)")
            if current_exam == 1:
                for drawing in drawings:
                    # 이미지 관련 정보 추출 시도
                    print(f"    이미지 #{image_count_in_doc}")
                    image_count_in_doc += 1

print(f"\n문서에서 찾은 이미지: {image_count_in_doc}개")
