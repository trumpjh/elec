import json
from docx import Document
import re

# JSON 로드
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# docx 로드
doc = Document('2025년도 문제.docx')
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

def extract_all_docx_problems():
    """docx에서 모든 문제 추출"""
    problems = {}
    current_exam = None
    
    for i, text in enumerate(paragraphs):
        # 회차 감지
        if '제' in text and '회' in text:
            match = re.search(r'제(\d+)회', text)
            if match:
                current_exam = f'제{match.group(1)}회'
            continue
        
        # 문제 찾기
        match = re.match(r'^(\d+)\.\s+(.+)$', text)
        if match and current_exam:
            problem_num = int(match.group(1))
            problem_key = (current_exam, problem_num)
            
            # 선택지 수집
            options = {}
            for offset in range(1, 5):
                if i + offset < len(paragraphs):
                    para = paragraphs[i + offset]
                    for symbol, idx in {'①': 0, '②': 1, '③': 2, '④': 3}.items():
                        if para.startswith(symbol):
                            option_text = para[1:].strip()
                            options[idx] = option_text
            
            # 4개 모두 찾지 못하면 한 줄로 된 경우 확인
            if len(options) < 4 and i + 1 < len(paragraphs):
                next_para = paragraphs[i + 1]
                if any(s in next_para for s in ['①', '②', '③', '④']):
                    option_pattern = r'[①②③④]\s*([^①②③④]+?)(?=[①②③④]|$)'
                    matches = re.findall(option_pattern, next_para)
                    options_list = [m.strip() for m in matches if m.strip()]
                    if len(options_list) == 4:
                        options = {i: opt for i, opt in enumerate(options_list)}
            
            if len(options) > 0:
                problems[problem_key] = [options.get(i, '') for i in range(4)]
    
    return problems

docx_problems = extract_all_docx_problems()

print("="*80)
print("JSON과 DOCX 선택지 비교 (내용이 다른 문제 찾기)")
print("="*80)

mismatches = []

for q in data['questions']:
    if len(q['options']) == 4:  # 선택지가 4개인 경우만 비교
        key = (q['exam'], q['number'])
        
        if key in docx_problems:
            docx_opts = docx_problems[key]
            json_opts = q['options']
            
            # 정확히 일치하지 않으면
            if json_opts != docx_opts:
                mismatches.append({
                    'exam': q['exam'],
                    'number': q['number'],
                    'question': q['question'],
                    'json': json_opts,
                    'docx': docx_opts
                })

print(f"\n발견된 불일치: {len(mismatches)}개\n")

for i, mismatch in enumerate(mismatches, 1):
    print(f"\n{'='*80}")
    print(f"{i}. {mismatch['exam']} 문제 {mismatch['number']}")
    print(f"{'='*80}")
    print(f"문제: {mismatch['question'][:70]}...")
    
    print(f"\n📄 JSON 선택지:")
    for j, opt in enumerate(mismatch['json'], 1):
        print(f"  {j}. {opt[:60]}")
    
    print(f"\n📋 DOCX 선택지:")
    for j, opt in enumerate(mismatch['docx'], 1):
        print(f"  {j}. {opt[:60]}")
    
    # 어떤 부분이 다른지 표시
    print(f"\n⚠️  차이점:")
    for j in range(4):
        if j < len(mismatch['json']) and j < len(mismatch['docx']):
            if mismatch['json'][j] != mismatch['docx'][j]:
                print(f"  선택지 {j+1}: JSON과 DOCX가 다름")
                if len(mismatch['json'][j]) < 80 and len(mismatch['docx'][j]) < 80:
                    print(f"    JSON: {mismatch['json'][j]}")
                    print(f"    DOCX: {mismatch['docx'][j]}")

if mismatches:
    print(f"\n{'='*80}")
    print(f"총 {len(mismatches)}개 문제에서 선택지가 다릅니다")
    print("="*80)
else:
    print("\n✅ 모든 선택지가 일치합니다!")
