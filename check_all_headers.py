from docx import Document
import re

doc = Document('2025년도 설명.docx')

# 모든 헤더 찾기
headers = []
for element in doc.element.body:
    if element.tag.endswith('p'):
        text = ''.join([t.text for t in element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
        
        if '회' in text and '설명' in text:
            match = re.search(r'제(\d)회.*설명', text)
            if match:
                headers.append(f"제{match.group(1)}회 설명")

print("문서의 설명 섹션들:")
for i, h in enumerate(headers):
    print(f"  {i}: {h}")

print(f"\n총 {len(headers)}개의 설명 섹션")
