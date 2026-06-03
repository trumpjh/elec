from docx import Document
import json
import re

# 설명 추출
doc = Document('2025년도 설명.docx')
explanations = []
current_explanation = None

for para in doc.paragraphs:
    text = para.text.strip()
    if not text:
        continue
    
    # 단원명 확인 (첫 글자가 단원명일 때)
    if text in ['전기설비', '전기기기', '전기공학']:
        if current_explanation:
            explanations.append(current_explanation)
        current_explanation = {'category': text, 'text': ''}
    elif current_explanation is not None:
        if current_explanation['text']:
            current_explanation['text'] += '\n' + text
        else:
            current_explanation['text'] = text

if current_explanation:
    explanations.append(current_explanation)

print(f"총 추출된 설명: {len(explanations)}")
print("\n처음 5개 설명:")
for i, exp in enumerate(explanations[:5]):
    print(f"\n설명 #{i+1}")
    print(f"Category: {exp['category']}")
    print(f"Text: {exp['text'][:100]}...")
