"""
2025년도 문제.docx 파일에서 이미지를 찾아서 분석
"""

from docx import Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
import re
from pathlib import Path
import os

def iter_block_items(parent):
    """문서의 모든 블록 요소 순회 (문단, 표, 이미지 포함)"""
    if isinstance(parent, _Cell):
        parent_elm = parent._element
    else:
        parent_elm = parent._element
    for child in parent_elm:
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def extract_images_from_paragraph(paragraph, para_index):
    """문단에서 이미지 추출"""
    images = []
    for rel in paragraph.part.rels.values():
        if "image" in rel.target_ref:
            images.append({
                'type': 'paragraph',
                'para_index': para_index,
                'rel_id': rel.rId,
                'target': rel.target_ref
            })
    return images

def extract_images_from_docx(filepath):
    """docx에서 모든 이미지 추출"""
    doc = Document(filepath)
    
    print("\n" + "="*70)
    print("📊 문제.docx 이미지 분석")
    print("="*70)
    
    all_items = []
    para_counter = 0
    current_exam = None
    current_problem_num = None
    
    # 1단계: 모든 블록 요소 순회
    for item in iter_block_items(doc):
        if isinstance(item, Paragraph):
            text = item.text.strip()
            all_items.append({
                'type': 'paragraph',
                'index': para_counter,
                'text': text,
                'item': item
            })
            
            # 회차 감지
            if '제' in text and '회' in text:
                match = re.search(r'제(\d+)회', text)
                if match:
                    current_exam = f'제{match.group(1)}회'
            
            # 문제 번호 감지
            match = re.match(r'^(\d+)\.\s+', text)
            if match:
                current_problem_num = int(match.group(1))
            
            para_counter += 1
        elif isinstance(item, Table):
            all_items.append({
                'type': 'table',
                'index': para_counter,
                'item': item
            })
            para_counter += 1
    
    print(f"\n총 요소: {len(all_items)}개")
    
    # 2단계: 이미지 찾기
    print("\n【이미지가 있는 문제】")
    print("-" * 70)
    
    images_found = []
    
    for item in all_items:
        if item['type'] == 'paragraph':
            para = item['item']
            # 문단의 이미지 확인 (runs에 drawing 확인)
            has_image = False
            
            for run in para.runs:
                # inline shape 확인
                if run._element.drawing_lst:
                    has_image = True
                    break
            
            if has_image:
                # 이 문단 근처의 문제 찾기
                text = item['text']
                print(f"\n📍 인덱스 {item['index']}: {text[:60] if text else '[이미지]'}...")
                
                # 이전 문단에서 문제 번호 찾기
                for prev_item in reversed(all_items[:item['index']]):
                    if prev_item['type'] == 'paragraph':
                        match = re.match(r'^(\d+)\.\s+(.+)$', prev_item['text'])
                        if match:
                            problem_num = int(match.group(1))
                            problem_text = match.group(2)
                            
                            # 회차 찾기
                            for exam_item in reversed(all_items[:prev_item['index']]):
                                if exam_item['type'] == 'paragraph':
                                    exam_match = re.search(r'제(\d+)회', exam_item['text'])
                                    if exam_match:
                                        exam = f'제{exam_match.group(1)}회'
                                        print(f"   → {exam} 문제 {problem_num}")
                                        print(f"   → 문제: {problem_text[:50]}...")
                                        images_found.append({
                                            'exam': exam,
                                            'number': problem_num,
                                            'text': problem_text
                                        })
                                        break
                            break
        
        elif item['type'] == 'table':
            table = item['item']
            # 표의 셀에 이미지가 있는지 확인
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        has_image = any(run._element.drawing_lst for run in para.runs)
                        if has_image:
                            print(f"\n📍 표에 이미지 발견 (인덱스 {item['index']})")
    
    print(f"\n\n【이미지 포함 문제 요약】")
    print("-" * 70)
    print(f"총 {len(images_found)}개 문제에 이미지 포함\n")
    
    for img in images_found:
        print(f"  {img['exam']} 문제 {img['number']}")
    
    return images_found

# 실행
images_with_problems = extract_images_from_docx('2025년도 문제.docx')
