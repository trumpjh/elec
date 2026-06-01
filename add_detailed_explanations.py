import json

# questions_2025_full.json 읽기
with open('questions_2025_full.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']

# 각 문제에 대한 상세 설명 추가
enhanced_explanations = {
    1: "진동이 있는 환경에서 전선 접속 시 일반 너트와 볼트만으로는 진동에 의해 풀어질 수 있습니다.\n스프링 와셔(스프링 추 와셔)는 스프링력에 의해 항상 너트에 압력을 가하므로 진동에 의한 이완을 방지합니다.\n- 스프링 와셔: 탄성력으로 헐거워짐 방지\n- 이중너트: 두 개의 너트를 사용하여 잠금",
    
    2: "심벌도(도면 기호)에서 EQ는 지진감지기를 나타냅니다.\n- EQ: Earthquake Detector (지진감지기)\n- 기타 심벌들: 변압기(T), 누전경보기(GFCI), 전류제한기 등",
    
    3: "접지시스템은 전기 안전을 위해 설치되는데, 다음과 같이 분류됩니다.\n- 단독접지: 각 기기마다 개별적으로 접지극 설치\n- 공통접지: 여러 기기가 하나의 접지극 공유\n- 통합접지: 단독접지와 공통접지를 함께 활용\n- 보호접지: 금속제 외함이나 노출도전부를 접지하는 방식",
    
    4: "철심 손실은 와류손과 히스테리시스손으로 구성됩니다.\n- 와류손(Eddy loss): 교변 자속에 의해 유도된 유도전류로 인한 손실\n  - 해결책: 얇은 강판을 여러 겹으로 겹쳐 성층철심 사용\n- 히스테리시스손(Hysteresis loss): 자성재료의 자화 특성으로 인한 손실\n  - 해결책: 규소강판(Silicon Steel) 사용으로 자기 특성 개선",
    
    11: "전선 접속용 슬리브는 다음과 같은 종류가 있습니다.\n- C형: 표준형\n- E형: 압착 연장형\n- P형: 절연관 삽입형\n- S형: 단면 슬리브\n- 주의: D형은 존재하지 않습니다.",
    
    12: "3상 유도전동기의 원선도 작성에 필요한 시험:\n- 저항 측정: 권선 저항 측정\n- 무부하 시험: 회전손(철손, 마찰손, 풍손) 측정\n- 구속 시험: 고정자 회전자를 고정하고 정격전류 통과 시 전압, 전류, 전력 측정\n- 슬립 측정: 원선도 작성에 직접 필요하지 않음 (이미 이론으로 계산됨)",
    
    14: "금속몰드 공사 기준:\n- 지지점 간 거리: 1.5[m] 이하\n- 조영재: 1/5[m] 이하마다 고정\n- 사용전압: 400[V] 이하\n- 설치 장소: 옥내의 외상을 받을 우려가 없는 건조한 노출장소\n- 접지공사 필수\n- 금속몰드와 박스 접속 시 부싱 사용",
    
    15: "직류기의 구조:\n- 자극편: 계자역할, 영구자석 또는 전자석\n- 정류자(Commutator): 교류를 직류로 정류\n- 공극: 자극편과 전기자 사이의 공간\n- 브러시: 정류자와 접촉하여 전기자 권선과 외부회로 연결\n- 전기자(Armature): 회전자 코일",
    
    16: "금속관 공사 부속품:\n- 링 리듀서: 관의 지름이 박스보다 클 때 사용 (관→박스 감소)\n- 부싱: 금속관 끝부분에 사용\n- 커넥터: 금속관 상호 접속\n- 로크너트: 너트를 고정하는 잠금 너트",
    
    20: "활선 공사용 안전공구:\n- 전선 피박기(Wire Peeler): 활선 상태에서 절연피복을 벗기는 도구\n- 와이어 통: 전선을 움직일 때 사용\n- 데드 엔드 커버: 전선 끝 보호\n- 애자 커버: 애자 보호",
    
    22: "피뢰시스템 접지도체 기준:\n- 구리선: 16[mm²] 이상\n- 철선: 50[mm²] 이상\n- 접지도체와 접지극의 접속: 발열성 용접 사용\n- 접지저항: 10[Ω] 이하 권장",
}

# 설명 업데이트
for q in questions:
    q_num = q['number']
    if q_num in enhanced_explanations:
        # 기존 설명이 없거나 너무 짧으면 새로운 설명으로 교체
        if not q['explanation'] or len(q['explanation']) < 30:
            q['explanation'] = enhanced_explanations[q_num]
        else:
            # 기존 설명에 상세내용 추가
            q['explanation'] = q['explanation'] + "\n\n[상세 설명]\n" + enhanced_explanations[q_num]

# 업데이트된 데이터 저장
output = {
    'total': len(questions),
    'updated_date': '2025-06-01',
    'version': 'v2.0 - Enhanced with detailed explanations',
    'questions': questions
}

with open('questions_2025_enhanced.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✓ 상세 설명 추가 완료!")
print(f"✓ 총 {len(questions)}개 문제 처리")
print(f"✓ 파일 저장: questions_2025_enhanced.json")

# 샘플 출력
print("\n=== 샘플: 문제 1 ===")
print(f"Q: {questions[0]['question']}")
print(f"설명:\n{questions[0]['explanation']}")
