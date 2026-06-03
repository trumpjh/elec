from docx import Document

doc = Document('2025년도 설명.docx')

print("첫 50개 문단 (번호 포함):")
for i, para in enumerate(doc.paragraphs[:50]):
    text = para.text.strip()
    if text:
        print(f"{i}: '{text}'")
