from docx import Document
from docx.oxml import parse_xml
import os

doc = Document('2025년도 설명.docx')

# 모든 이미지를 추출할 디렉토리
os.makedirs('extracted_images', exist_ok=True)

image_count = 0

# 문서의 모든 요소를 순회
for rel in doc.part.rels.values():
    if "image" in rel.target_ref:
        image_part = rel.target_part
        image_bytes = image_part.blob
        
        # 파일 확장자 결정
        ext = image_part.partname.split('.')[-1]
        
        # 파일 이름
        image_name = f"extracted_image_{image_count}.{ext}"
        image_path = os.path.join('extracted_images', image_name)
        
        # 이미지 저장
        with open(image_path, 'wb') as f:
            f.write(image_bytes)
        
        image_count += 1
        print(f"추출됨: {image_name}")

print(f"\n총 {image_count}개 이미지 추출됨")
