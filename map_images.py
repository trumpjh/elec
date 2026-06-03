"""
이미지 파일을 문제와 설명에 매핑하는 스크립트
"""

import json
import re
from pathlib import Path
from collections import defaultdict

def parse_image_filename(filename):
    """
    이미지 파일명으로부터 메타데이터 추출
    
    예시:
    - "2025년도 문제  제1회 60번.png" → {'type': 'problem', 'exam': '제1회', 'number': 60}
    - "2025년도 설명 제1회  44번.png" → {'type': 'explanation', 'exam': '제1회', 'number': 44}
    - "2025년도 제4회 문제 9번.png" → {'type': 'problem', 'exam': '제4회', 'number': 9}
    """
    
    # 파일 확장자 제거
    name = Path(filename).stem
    
    # 문제 vs 설명 구분 (먼저 제거할 부분 파악)
    image_type = None
    if '설명' in name:
        image_type = 'explanation'
    elif '문제' in name:
        image_type = 'problem'
    else:
        return None
    
    # 회차와 문제 번호 먼저 추출 (메타데이터 추출)
    match = re.search(r'제(\d+)회(?:\s+문제\s+|\s+)(\d+)번', name)
    if not match:
        return None
    
    exam_num = int(match.group(1))
    problem_num = int(match.group(2))
    
    return {
        'type': image_type,
        'exam': f'제{exam_num}회',
        'number': problem_num,
        'filename': filename
    }


def map_images_to_questions():
    """이미지를 문제에 매핑"""
    print("\n" + "="*60)
    print("🖼️  이미지 매핑 시작")
    print("="*60)
    
    # 이미지 폴더 스캔
    images_dir = Path('images')
    image_files = list(images_dir.glob('*.*'))
    
    print(f"\n📁 찾은 이미지: {len(image_files)}개")
    
    # 이미지 파싱
    problem_images = defaultdict(list)  # {(exam, number): [filename]}
    explanation_images = defaultdict(list)
    
    for image_file in sorted(image_files):
        filename = image_file.name
        meta = parse_image_filename(filename)
        
        if meta:
            key = (meta['exam'], meta['number'])
            if meta['type'] == 'problem':
                problem_images[key].append(meta['filename'])
                print(f"   ✓ {meta['exam']} 문제 {meta['number']}: {filename}")
            else:
                explanation_images[key].append(meta['filename'])
                print(f"   ✓ {meta['exam']} 설명 {meta['number']}: {filename}")
        else:
            print(f"   ⚠️  분석 불가: {filename}")
    
    print(f"\n📊 매핑 결과:")
    print(f"   문제 이미지: {sum(len(v) for v in problem_images.values())}개")
    print(f"   설명 이미지: {sum(len(v) for v in explanation_images.values())}개")
    
    # questions.json 로드
    with open('questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['questions']
    
    # 문제에 이미지 정보 추가
    added_problem_images = 0
    added_explanation_images = 0
    
    for q in questions:
        key = (q['exam'], q['number'])
        
        # 문제 이미지 추가
        if key in problem_images:
            # 여러 이미지가 있으면 첫 번째 사용
            q['image'] = f"images/{problem_images[key][0]}"
            added_problem_images += 1
            if len(problem_images[key]) > 1:
                q['extra_images'] = [f"images/{img}" for img in problem_images[key][1:]]
        
        # 설명 이미지 추가
        if key in explanation_images:
            if 'explanation' not in q:
                q['explanation'] = ''
            # explanation_image 필드 추가
            q['explanation_image'] = f"images/{explanation_images[key][0]}"
            added_explanation_images += 1
            if len(explanation_images[key]) > 1:
                q['extra_explanation_images'] = [f"images/{img}" for img in explanation_images[key][1:]]
    
    # 업데이트된 questions.json 저장
    with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 이미지 매핑 완료:")
    print(f"   문제 이미지 추가: {added_problem_images}개")
    print(f"   설명 이미지 추가: {added_explanation_images}개")
    
    # 통계
    with_problem_image = sum(1 for q in questions if q.get('image'))
    with_explanation_image = sum(1 for q in questions if q.get('explanation_image'))
    
    print(f"\n📈 최종 통계:")
    print(f"   총 문제: {len(questions)}개")
    print(f"   문제 이미지 있음: {with_problem_image}개")
    print(f"   설명 이미지 있음: {with_explanation_image}개")
    
    # 회차별 이미지 통계
    print(f"\n📋 회차별 이미지 수:")
    by_exam = defaultdict(lambda: {'total': 0, 'problem_img': 0, 'exp_img': 0})
    
    for q in questions:
        exam = q['exam']
        by_exam[exam]['total'] += 1
        if q.get('image'):
            by_exam[exam]['problem_img'] += 1
        if q.get('explanation_image'):
            by_exam[exam]['exp_img'] += 1
    
    for exam in sorted(by_exam.keys()):
        stats = by_exam[exam]
        print(f"   {exam}: {stats['total']}개 (문제 {stats['problem_img']}개, 설명 {stats['exp_img']}개)")
    
    return data


if __name__ == '__main__':
    try:
        map_images_to_questions()
        print("\n" + "="*60)
        print("✅ questions.json 이미지 매핑 완료!")
        print("="*60)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
