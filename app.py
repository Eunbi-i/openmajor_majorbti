import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="자유전공학부 전공 MBTI 테스트",
    page_icon="🎓",
    layout="centered"
)

# 16가지 유형별 정보 및 학과 매핑 데이터
TYPE_INFO = {
    "SAMG": {
        "title": "🏛️ 글로벌 리더형",
        "desc": "사회적 현상을 논리적으로 분석하며, 정책·공공 분야 및 국제 관계를 다루는 데 강점이 있습니다.",
        "depts": ["정치외교학과", "행정학과", "무역학과"]
    },
    "SAML": {
        "title": "📊 비즈니스 데이터 전략가",
        "desc": "시장과 기업의 데이터를 분석하고 조직의 시스템 및 수치를 효율적으로 관리합니다.",
        "depts": ["경영학과", "회계학과", "경영정보학과"]
    },
    "SACG": {
        "title": "🎬 미디어 트렌드 세터",
        "desc": "사회 트렌드와 대중 문화를 재빨리 캐치하여 콘텐츠, 미디어, 관광 상품을 기획합니다.",
        "depts": ["언론홍보학과", "관광경영학과", "관광개발학과"]
    },
    "SACL": {
        "title": "🤝 인간 중심 서비스 전문가",
        "desc": "사람들의 삶의 질, 사회적 환경, 패션 및 라이프스타일을 섬세하게 케어하고 창의적으로 표현합니다.",
        "depts": ["사회학과", "생활환경복지학과", "패션의류학과"]
    },
    "SRMG": {
        "title": "📜 인문학적 사색가",
        "desc": "언어, 역사, 철학 등 인간과 사회의 근본적인 사상과 가치를 깊이 있게 탐구합니다.",
        "depts": ["국어국문학과", "사학과", "철학과"]
    },
    "SRML": {
        "title": "🌐 글로벌 언어·문화 전문가",
        "desc": "세계 여러 나라의 언어와 독특한 문학, 문화를 깊이 탐구하고 글로벌 감각을 키웁니다.",
        "depts": ["영어영문학과", "독어독문학과", "일어일문학과", "중어중문학과"]
    },
    "SRCG": {
        "title": "📈 공공 경제 전문가",
        "desc": "국가와 시장 전체의 경제 흐름을 분석하고 사회적 자원의 효율적 배분을 연구합니다.",
        "depts": ["경제학과"]
    },
    "SRCL": {
        "title": "⚓ 해양 공공 안전 기획자",
        "desc": "바다라는 특수 환경에서 공공의 안전, 법률, 해양 행정 업무를 전문적으로 수행합니다.",
        "depts": ["해양산업경찰학과"]
    },
    "TAMG": {
        "title": "💻 미래 첨단 ICT 엔지니어",
        "desc": "IT 시스템, 소프트웨어, 통신 및 전자 기술을 바탕으로 디지털 미래를 설계합니다.",
        "depts": ["컴퓨터공학과", "통신공학과", "전자공학과"]
    },
    "TAML": {
        "title": "⚙️ 스마트 에너지·메카 닥터",
        "desc": "기계, 전기, 원자력, 에너지 시스템 등 산업의 핵심 파워를 구축하고 제어합니다.",
        "depts": ["전기공학과", "기계시스템공학과", "원자력공학과", "화공그린에너지학과"]
    },
    "TACG": {
        "title": "🏗️ 친환경 공간·도시 디자이너",
        "desc": "인간이 살아가는 건축물과 도시 공간, 자연 환경을 아름답고 안전하게 설계합니다.",
        "depts": ["건축공학과", "건축학과", "토목공학과", "환경공학과"]
    },
    "TACL": {
        "title": "🌱 스마트 융합 농업 기획자",
        "desc": "첨단 IT 및 바이오 기술을 농업 및 생명 자원에 결합하여 미래 먹거리를 창출합니다.",
        "depts": ["스마트팜학부", "산업응용경제학과"]
    },
    "TRMG": {
        "title": "📐 기초 수리·물리 탐구자",
        "desc": "우주와 자연계의 근본 법칙을 수학적 논리와 수식으로 파헤치는 수리적 탐구자입니다.",
        "depts": ["수학과", "물리학과"]
    },
    "TRML": {
        "title": "🧬 생명 바이오 연구원",
        "desc": "동식물, 미생물, 유전자 등 모든 생명 현상의 비밀을 밝히고 바이오 기술을 다룹니다.",
        "depts": ["생물학과", "식물자원환경전공", "원예과학전공", "바이오소재전공", "분자생명공학전공", "동물생명공학전공"]
    },
    "TRCG": {
        "title": "🌊 해양·지구 환경 과학자",
        "desc": "지구와 바다 생태계, 수산 자원의 원리를 연구하고 해양 생태계를 보존합니다.",
        "depts": ["해양생명과학과", "지구해양과학과", "수산생명의학과", "해양시스템공학과"]
    },
    "TRCL": {
        "title": "🧪 코스메틱·식품 융합 연구원",
        "desc": "일상생활과 밀접한 화장품, 식품, 영양 및 화학 물질을 연구·개발합니다.",
        "depts": ["화학코스메틱학과", "식품영양학과", "식품생명공학과"]
    }
}

# 질문 문항 및 선택지 (12문항)
questions = [
    {
        "question": "Q1. 뉴스나 유튜브를 볼 때 더 끌리는 주제는?",
        "options": [
            ("사회적 이슈, 사건 사고, 문화 트렌드, 사람들의 이야기", "S"),
            ("새로운 IT 기술, 우주/과학 신기술, 자연 현상의 비밀", "T")
        ]
    },
    {
        "question": "Q2. 해결해보고 싶은 인류의 문제는?",
        "options": [
            ("사회적 불평등, 국가 간 갈등, 문화적 소외 문제", "S"),
            ("기후 변화, 질병 치료제 개발, 에너지 부족 문제", "T")
        ]
    },
    {
        "question": "Q3. 학창 시절 더 친숙하게 느껴졌던 과목은?",
        "options": [
            ("국어, 사회, 역사, 외국어", "S"),
            ("수학, 물리학, 화학, 지구과학, 정보", "T")
        ]
    },
    {
        "question": "Q4. 새로운 프로젝트를 시작할 때 나의 방식은?",
        "options": [
            ("관련 데이터와 논문, 기존 이론부터 철저히 분석한다.", "A"),
            ("일단 다양한 아이디어를 떠올리고 실질적으로 적용해 본다.", "C")
        ]
    },
    {
        "question": "Q5. 나의 주장을 설득력 있게 만드는 핵심 요소는?",
        "options": [
            ("수치화된 통계 자료와 체계적 논리", "A"),
            ("현실적인 적용 가능성과 직관적인 아이디어", "C")
        ]
    },
    {
        "question": "Q6. 시험을 준비할 때 나의 공부 스타일은?",
        "options": [
            ("전체적인 개념의 체계와 원리를 원론적으로 이해한다.", "A"),
            ("기출문제를 풀며 문제 유형을 익히고 실전에 바로 적용한다.", "C")
        ]
    },
    {
        "question": "Q7. 공부를 통해 얻고자 하는 목적은?",
        "options": [
            ("거시적인 시스템, 조직, 사회적 구조를 관리하고 운영하는 것", "M"),
            ("세상이나 생명체, 인간의 근본적인 원리를 밝혀내는 깊이 있는 탐구", "R")
        ]
    },
    {
        "question": "Q8. 팀 프로젝트를 할 때 내가 더 잘할 수 있는 역할은?",
        "options": [
            ("전체 일정과 시스템을 조정하고 종합하는 총괄 관리자", "M"),
            ("한 주제를 맡아 깊이 있게 자료를 수집하고 분석하는 전문 탐구자", "R")
        ]
    },
    {
        "question": "Q9. 더 흥미를 느끼는 연구 대상은?",
        "options": [
            ("기업, 국가, 법, 기술 시스템 등 사회적으로 구축된 구조", "M"),
            ("자연, 인간의 마음, 언어, 유전자 등 근본적으로 존재하는 대상", "R")
        ]
    },
    {
        "question": "Q10. 미래에 활약하고 싶은 무대는?",
        "options": [
            ("글로벌 시장이나 공공기관 등 넓은 범주에 영향을 미치는 곳", "G"),
            ("특수 기술이나 특정 산업 분야에서 독보적인 영역을 구축하는 곳", "L")
        ]
    },
    {
        "question": "Q11. 내가 선택할 강의의 범위는?",
        "options": [
            ("인문, 사회, 경제 등 폭넓은 시야와 통찰을 주는 과목", "G"),
            ("특정 기계, 바이오, 화학 등 뾰족한 기술을 배우는 과목", "L")
        ]
    },
    {
        "question": "Q12. 더 가치 있게 여겨지는 것은?",
        "options": [
            ("다양성, 공공의 이익, 글로벌 감각", "G"),
            ("전문성, 기술적 완성도, 실용적 활용성", "L")
        ]
    }
]

# 세션 상태 초기화 (페이지 이동 및 답변 저장용)
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# 앱 헤더
st.title("🎓 자유전공학부 전공 MBTI 테스트")
st.caption("고등학생을 위한 맞춤형 전공 탐색 프로그램 | 단계별 테스트")
st.markdown("---")

total_q = len(questions)

# ------------------------------------
# 1. 질문 진행 화면 (step < total_q)
# ------------------------------------
if st.session_state.step < total_q:
    current_idx = st.session_state.step
    q_data = questions[current_idx]
    
    # 진행률 표시
    progress = (current_idx + 1) / total_q
    st.progress(progress)
    st.write(f"**질문 {current_idx + 1} / {total_q}**")
    
    st.subheader(q_data["question"])
    
    # 기본 선택 항목 복원 (이전 버튼 눌렀을 때)
    default_choice = st.session_state.answers.get(current_idx, 0)
    
    choice = st.radio(
        "선택지를 골라주세요:",
        options=[opt[0] for opt in q_data["options"]],
        index=default_choice,
        key=f"q_{current_idx}"
    )
    
    st.write("")
    col1, col2 = st.columns([1, 1])
    
    # 이전 버튼
    with col1:
        if current_idx > 0:
            if st.button("⬅️ 이전 질문"):
                # 현재 선택 저장
                selected_code = q_data["options"][[opt[0] for opt in q_data["options"]].index(choice)][1]
                selected_idx = [opt[0] for opt in q_data["options"]].index(choice)
                st.session_state.answers[current_idx] = selected_idx
                
                st.session_state.step -= 1
                st.rerun()

    # 다음/결과보기 버튼
    with col2:
        btn_label = "🔥 결과 확인하기" if current_idx == total_q - 1 else "다음 질문 ➡️"
        if st.button(btn_label):
            selected_idx = [opt[0] for opt in q_data["options"]].index(choice)
            st.session_state.answers[current_idx] = selected_idx
            st.session_state.step += 1
            st.rerun()

# ------------------------------------
# 2. 결과 출력 화면 (step == total_q)
# ------------------------------------
else:
    # 점수 집계
    scores = {"S": 0, "T": 0, "A": 0, "C": 0, "M": 0, "R": 0, "G": 0, "L": 0}
    
    for i, ans_idx in st.session_state.answers.items():
        code = questions[i]["options"][ans_idx][1]
        scores[code] += 1

    # 퍼센트 계산 (각 축 당 3문항)
    pct_S = round((scores["S"] / 3) * 100)
    pct_T = 100 - pct_S
    
    pct_A = round((scores["A"] / 3) * 100)
    pct_C = 100 - pct_A
    
    pct_M = round((scores["M"] / 3) * 100)
    pct_R = 100 - pct_M
    
    pct_G = round((scores["G"] / 3) * 100)
    pct_L = 100 - pct_G

    # 최종 MBTI 조합
    mbti = ""
    mbti += "S" if scores["S"] >= scores["T"] else "T"
    mbti += "A" if scores["A"] >= scores["C"] else "C"
    mbti += "M" if scores["M"] >= scores["R"] else "R"
    mbti += "G" if scores["G"] >= scores["L"] else "L"

    result_data = TYPE_INFO.get(mbti, TYPE_INFO["SAMG"])

    st.balloons()
    
    st.markdown("### 🎯 당신의 성격 유형은:")
    st.title(f"✨ {result_data['title']} ({mbti})")
    
    st.info(result_data["desc"])

    st.markdown("---")
    st.subheader("📊 4개 영역별 성향 지표")
    st.caption("선택하신 답변을 바탕으로 한 영역별 비율입니다.")

    # 1. S vs T
    col_a, col_b = st.columns([1, 1])
    col_a.write(f"**사회/인간 (S)**: {pct_S}%")
    col_b.write(f"**기술/자연 (T)**: {pct_T}%")
    st.progress(pct_S / 100)

    # 2. A vs C
    col_a, col_b = st.columns([1, 1])
    col_a.write(f"**분석/논리 (A)**: {pct_A}%")
    col_b.write(f"**창의/응용 (C)**: {pct_C}%")
    st.progress(pct_A / 100)

    # 3. M vs R
    col_a, col_b = st.columns([1, 1])
    col_a.write(f"**경영/시스템 (M)**: {pct_M}%")
    col_b.write(f"**연구/자연 (R)**: {pct_R}%")
    st.progress(pct_M / 100)

    # 4. G vs L
    col_a, col_b = st.columns([1, 1])
    col_a.write(f"**글로벌/공공 (G)**: {pct_G}%")
    col_b.write(f"**전문/기술 (L)**: {pct_L}%")
    st.progress(pct_G / 100)

    st.markdown("---")
    st.markdown("### 📚 추천 전공 트랙 (자유전공 진학 시 선택 가능 학과)")
    for dept in result_data["depts"]:
        st.markdown(f"- **{dept}**")

    st.success("""
    💡 **자유전공학부의 특별함!**
    지금 나온 결과가 마음에 들거나, 혹은 여러 학과 사이에서 고민되나요?
    자유전공학부에 입학하면 **1학년 동안 이 학과들의 수업을 직접 들어보고**
    나에게 정말 맞는 전공을 2학년 때 자유롭게 선택할 수 있습니다!
    """)

    # 다시 하기 버튼
    if st.button("🔄 테스트 다시 하기"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
