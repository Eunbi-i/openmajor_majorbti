import os
import glob
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="전공탐색 MBTI",
    page_icon="🎓",
    layout="centered"
)

# 🎨 디자인 커스텀 CSS
st.markdown("""
<style>
    /* 상단 헤더 스타일 */
    .header-sub1 {
        font-size: 15px !important;
        color: #a0a0a0 !important;
        margin-bottom: 4px !important;
    }
    .custom-title {
        font-size: 30px !important;
        font-weight: 800 !important;
        margin-top: 4px !important;
        margin-bottom: 4px !important;
        line-height: 1.2 !important;
    }
    .header-sub2 {
        font-size: 14px !important;
        color: #808080 !important;
        margin-bottom: 16px !important;
    }
    
    /* 결과 제목 스타일 */
    .result-title {
        font-size: 22px !important;
        font-weight: 700 !important;
        margin-top: 8px !important;
        margin-bottom: 16px !important;
    }

    /* 모바일 대응 성향 지표 Flexbox */
    .indicator-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        font-size: 15px;
        margin-bottom: 4px;
    }
    .indicator-left {
        font-weight: bold;
        text-align: left;
    }
    .indicator-right {
        font-weight: bold;
        text-align: right;
    }

    /* 모바일에서도 버튼 2개가 가로로 50%씩 고정되도록 설정 */
    div[data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
    }
</style>
""", unsafe_allow_html=True)

# 16가지 유형 매핑 데이터
TYPE_INFO = {
    "SAMG": {
        "title": "글로벌 리더형",
        "desc": "사회적 현상을 논리적으로 분석하며, 정책·공공 분야 및 국제 관계를 다루는 데 강점이 있습니다.",
        "depts": ["사회과학대학 정치외교학과", "사회과학대학 행정학과", "경상대학 무역학과"]
    },
    "SAML": {
        "title": "비즈니스 데이터 전략가",
        "desc": "시장과 기업의 데이터를 분석하고 조직의 시스템 및 수치를 효율적으로 관리합니다.",
        "depts": ["경상대학 경영학과", "경상대학 회계학과", "경상대학 경영정보학과"]
    },
    "SARG": {
        "title": "인문학적 사색가",
        "desc": "인간과 사회의 근본적인 사상, 언어, 역사를 논리적·학술적으로 깊이 탐구합니다.",
        "depts": ["인문대학 국어국문학과", "인문대학 사학과", "인문대학 철학과"]
    },
    "SARL": {
        "title": "글로벌 언어·문화 전문가",
        "desc": "세계 여러 나라의 언어와 문학을 체계적으로 연구하고 글로벌 감각을 키웁니다.",
        "depts": ["인문대학 영어영문학과", "인문대학 독일학과", "인문대학 일어일문학과", "인문대학 중어중문학과"]
    },
    "SCMG": {
        "title": "미디어 트렌드 세터",
        "desc": "사회 트렌드와 대중 문화를 재빨리 캐치하여 콘텐츠, 미디어, 관광 상품을 기획합니다.",
        "depts": ["사회과학대학 언론홍보학과", "경상대학 관광경영학과", "경상대학 관광개발학과"]
    },
    "SCML": {
        "title": "인간 중심 서비스 전문가",
        "desc": "사람들의 삶의 질, 사회적 환경, 라이프스타일을 섬세하게 케어하고 창의적으로 표현합니다.",
        "depts": ["인문대학 사회학과", "자연과학대학 생활환경복지학과", "자연과학대학 패션의류학과"]
    },
    "SCRG": {
        "title": "공공 경제 전문가",
        "desc": "국가와 시장 전체의 경제 흐름을 독창적으로 분석하고 사회적 자원의 배분을 연구합니다.",
        "depts": ["사회과학대학 경제학과"]
    },
    "SCRL": {
        "title": "해양 공공 안전 기획자",
        "desc": "바다라는 특수 환경에서 공공의 안전, 법률, 해양 행정 업무를 창의적·실용적으로 수행합니다.",
        "depts": ["해양과학대학 해양산업경찰학과"]
    },
    "TAMG": {
        "title": "미래 첨단 ICT 엔지니어",
        "desc": "IT 시스템, 소프트웨어, 통신 및 전자 기술을 바탕으로 디지털 미래를 설계합니다.",
        "depts": ["공과대학 컴퓨터공학과", "공과대학 통신공학과", "공과대학 전자공학과"]
    },
    "TAML": {
        "title": "스마트 에너지·메카 닥터",
        "desc": "기계, 전기, 원자력, 에너지 시스템 등 산업의 핵심 파워를 구축하고 제어합니다.",
        "depts": ["공과대학 전기공학과", "공과대학 기계시스템공학과", "공과대학 원자력공학과", "공과대학 화공그린에너지학과"]
    },
    "TARG": {
        "title": "기초 수리·물리 탐구자",
        "desc": "우주와 자연계의 근본 법칙을 수학적 논리와 수식으로 파헤치는 수리적 탐구자입니다.",
        "depts": ["자연과학대학 수학과", "자연과학대학 물리학과"]
    },
    "TARL": {
        "title": "생명 바이오 연구원",
        "desc": "동식물, 미생물, 유전자 등 모든 생명 현상의 비밀을 밝히고 바이오 기술을 다룹니다.",
        "depts": [
            "자연과학대학 생물학과",
            "생명자원과학대학 스마트팜학부 식물자원환경전공",
            "생명자원과학대학 스마트팜학부 원예과학전공",
            "생명자원과학대학 생명공학부 바이오소재전공",
            "생명자원과학대학 생명공학부 분자생명공학전공",
            "생명자원과학대학 생명공학부 동물생명공학전공"
        ]
    },
    "TCMG": {
        "title": "친환경 공간·도시 디자이너",
        "desc": "인간이 살아가는 건축물과 도시 공간을 안전하고 아름답게 기획·설계합니다.",
        "depts": ["공과대학 건축공학과", "공과대학 건축학과", "공과대학 토목공학과"]
    },
    "TCML": {
        "title": "스마트 융합 농업 기획자",
        "desc": "첨단 IT 및 바이오 기술을 농업 및 생명 자원에 창의적으로 결합하여 미래 먹거리를 창출합니다.",
        "depts": ["생명자원과학대학 산업응용경제학과"]
    },
    "TCRG": {
        "title": "해양·지구 환경 과학자",
        "desc": "지구와 바다 생태계, 수산 자원 및 환경 오염의 원리를 탐구하고 생태계를 보존하는 아이디어를 냅니다.",
        "depts": [
            "해양과학대학 해양생명과학과",
            "해양과학대학 지구해양과학과",
            "해양과학대학 수산생명의학과",
            "해양과학대학 해양시스템공학과",
            "해양과학대학 환경공학과"
        ]
    },
    "TCRL": {
        "title": "코스메틱·식품 융합 연구원",
        "desc": "일상생활과 밀접한 화장품, 식품, 영양 및 화학 물질을 실용적으로 연구·개발합니다.",
        "depts": [
            "자연과학대학 화학코스메틱학과",
            "자연과학대학 식품영양학과",
            "공과대학 식품생명공학과"
        ]
    }
}

# 20개 질문 문항
questions = [
    # [S vs T] (1~5)
    {
        "question": "Q1. 뉴스나 유튜브 알고리즘에 주로 떠오르는 관심 영상은?",
        "options": [
            ("요즘 핫한 이슈, 사회적 사건, 사람들의 심리나 문화 트렌드", "S"),
            ("최신 IT 기기 리뷰, 과학 신기술, 우주/자연 현상의 비밀", "T")
        ]
    },
    {
        "question": "Q2. 해결해보고 싶은 지구적/사회적 과제는?",
        "options": [
            ("빈부격차, 국가 간 갈등, 문화적 소외, 사회 안전망 구축", "S"),
            ("기후 변화, 신종 질병 치료제 개발, 에너지 부족, AI 기술 윤리", "T")
        ]
    },
    {
        "question": "Q3. 학창 시절 상대적으로 흥미를 느꼈던 수업 시간에 가까운 것은?",
        "options": [
            ("국어, 사회, 역사, 외국어 등 사람과 사회를 배우는 시간", "S"),
            ("수학, 물리학, 화학, 지구과학, 정보 등 원리와 공식을 배우는 시간", "T")
        ]
    },
    {
        "question": "Q4. 영화나 드라마를 볼 때 나도 모르게 더 집중하게 되는 부분은?",
        "options": [
            ("등장인물 간의 관계, 감정선, 사회적 메시지와 대사", "S"),
            ("세계관의 설정, 과학적/기술적 고증, 사건의 논리적 개연성", "T")
        ]
    },
    {
        "question": "Q5. 친구들과 대화할 때 더 즐거운 주제는?",
        "options": [
            ("최근 유행하는 밈, 연예/문화 이야기, 서로의 근황과 고민 상담", "S"),
            ("게임 메커니즘, 새로 나온 가전/IT 제품, 신기한 과학적 퀴즈", "T")
        ]
    },

    # [A vs C] (6~10)
    {
        "question": "Q6. 새로운 과제나 프로젝트를 시작할 때 나의 행동 방식은?",
        "options": [
            ("관련 자료, 기존 데이터, 성공 사례부터 철저히 분석하고 계획을 세운다.", "A"),
            ("일단 참신한 아이디어를 빠르게 떠올리고 즉시 시도해 보며 수정해 나간다.", "C")
        ]
    },
    {
        "question": "Q7. 내 주장을 다른 사람에게 설득할 때 가장 강력하다고 믿는 무기는?",
        "options": [
            ("객관적인 통계 수치, 논리적 근거, 잘 정리된 데이터", "A"),
            ("와닿는 예시, 직관적인 시각 자료, 참신하고 창의적인 아이디어", "C")
        ]
    },
    {
        "question": "Q8. 시험이나 과제를 준비할 때 나의 공부 스타일은?",
        "options": [
            ("개념의 체계와 기본 원리를 뿌리부터 정석대로 이해하는 편이다.", "A"),
            ("기출문제를 많이 풀면서 실전에 바로 적용하는 방식을 선호한다.", "C")
        ]
    },
    {
        "question": "Q9. 조별 과제를 할 때 내가 더 맡고 싶은 역할은?",
        "options": [
            ("자료 조사, 통계 분석, 전체적인 논리 흐름과 목차 잡기", "A"),
            ("PPT 발표 자료 디자인, 아이디어 회의 주도, 발표 연출하기", "C")
        ]
    },
    {
        "question": "Q10. 예상치 못한 문제나 오류에 부딪혔을 때 나의 반응은?",
        "options": [
            ("원인이 무엇인지 순서대로 차근차근 점검하며 논리적으로 풀어간다.", "A"),
            ("기존 틀을 벗어나 직관적이고 새로운 방식으로 대안을 찾아낸다.", "C")
        ]
    },

    # [M vs R] (11~15)
    {
        "question": "Q11. 내가 생각하는 학문과 공부의 궁극적인 목적은?",
        "options": [
            ("거시적인 시스템, 조직, 사회적 구조를 효율적으로 운영하고 관리하는 것", "M"),
            ("세상이나 생명체, 인간의 근본적인 원리와 본질을 깊이 있게 밝혀내는 것", "R")
        ]
    },
    {
        "question": "Q12. 팀을 이루어 일할 때 더 자신 있는 내 모습은?",
        "options": [
            ("전체 일정, 역할 분담, 자원 배분을 총괄하는 '시스템 관리자'", "M"),
            ("한 가지 세부 주제를 맡아 깊이 있게 파고드는 '전문 탐구자'", "R")
        ]
    },
    {
        "question": "Q13. 연구하거나 배워보고 싶은 대상에 더 가까운 것은?",
        "options": [
            ("기업, 국가, 법률, 시장, 기술 인프라 등 인간이 구축한 거시 시스템", "M"),
            ("자연 현상, 인간의 마음, 언어의 역사, 유전자 등 근본적으로 존재하는 대상", "R")
        ]
    },
    {
        "question": "Q14. 도서관이나 서점에 갔을 때 더 눈길이 가는 책의 종류는?",
        "options": [
            ("경영 전략, 트렌드 분석, 행정/정치, 리더십 관련 책", "M"),
            ("기초 과학, 철학, 역사적 사색, 생명과학 전문 서적", "R")
        ]
    },
    {
        "question": "Q15. 성과를 이루었을 때 더 큰 보람을 느끼는 순간은?",
        "options": [
            ("내가 기획하거나 관리한 시스템/조직이 원활하게 잘 돌아갈 때", "M"),
            ("아무도 밝혀내지 못한 새로운 사실이나 깊이 있는 원리를 깨달았을 때", "R")
        ]
    },

    # [G vs L] (16~20)
    {
        "question": "Q16. 미래에 내가 일하고 싶은 무대나 환경은?",
        "options": [
            ("글로벌 시장, 국제기구, 공공기관 등 넓은 범주에 영향력을 미치는 곳", "G"),
            ("특정 전문 기술이나 독보적인 산업 분야에서 최고의 전문가로 인정받는 곳", "L")
        ]
    },
    {
        "question": "Q17. 수강신청을 할 때 선호하는 과목의 스타일은?",
        "options": [
            ("인문, 사회, 경제 등 폭넓은 통찰력과 통섭적 시야를 길러주는 과목", "G"),
            ("특정 기계, 바이오, 화학, 실무 툴 등 뾰족한 기술과 전문 지식을 배우는 과목", "L")
        ]
    },
    {
        "question": "Q18. 내가 더 가치 있게 생각하는 나의 능력은?",
        "options": [
            ("다양한 분야를 연결하고 세상 전체의 흐름을 읽는 '넓은 시야'", "G"),
            ("한 분야의 기술이나 지식을 누구보다 깊게 다루는 '독보적 전문성'", "L")
        ]
    },
    {
        "question": "Q19. 어떤 일을 할 때 더 만족감을 느끼는가?",
        "options": [
            ("불특정 다수의 많은 사람들과 사회 전체에 긍정적 영향력을 줄 때", "G"),
            ("눈앞의 구체적인 문제나 기계/제품/기술을 완벽하게 해결하고 완성할 때", "L")
        ]
    },
    {
        "question": "Q20. 나를 표현하는 단어로 더 마음에 드는 것은?",
        "options": [
            ("시대를 읽고 세상을 연결하는 '글로벌 융합형 통섭가'", "G"),
            ("자신만의 영역이 확실한 '스페셜리스트(Specialist)'", "L")
        ]
    }
]

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# 헤더 정보
st.markdown('<div class="header-sub1">제주대학교 전공체험의 날 - 글로벌자율학부 자유전공 체험</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-title">🎓 전공탐색 MBTI TEST</div>', unsafe_allow_html=True)
st.markdown('<div class="header-sub2">개인 맞춤형 전공 탐색 및 추천 프로그램 | 총 20문항</div>', unsafe_allow_html=True)
st.markdown("---")

total_q = len(questions)

# ------------------------------------
# 1. 질문 진행 화면
# ------------------------------------
if st.session_state.step < total_q:
    current_idx = st.session_state.step
    q_data = questions[current_idx]
    
    progress = (current_idx + 1) / total_q
    st.progress(progress)
    st.write(f"**질문 {current_idx + 1} / {total_q}**")
    
    st.subheader(q_data["question"])
    st.write("선택지를 골라주세요:")
    
    selected_option = st.session_state.answers.get(current_idx, 0)
    
    for idx, (opt_text, code) in enumerate(q_data["options"]):
        is_selected = (selected_option == idx)
        prefix = "🔘 " if is_selected else "⚪ "
        btn_text = f"{prefix}{opt_text}"
        btn_type = "primary" if is_selected else "secondary"
        
        if st.button(btn_text, key=f"opt_{current_idx}_{idx}", use_container_width=True, type=btn_type):
            st.session_state.answers[current_idx] = idx
            st.rerun()

    st.write("")
    
    # 📌 요청사항 1: 이전/다음 버튼을 모바일에서도 50:50으로 나란히 가로 배치
    col1, col2 = st.columns(2)
    
    with col1:
        if current_idx > 0:
            if st.button("⬅️ 이전 질문", use_container_width=True):
                st.session_state.step -= 1
                st.rerun()
        else:
            st.write("")  # 첫 번째 질문일 때 공간 유지

    with col2:
        btn_label = "🔥 결과 확인하기" if current_idx == total_q - 1 else "다음 질문 ➡️"
        if st.button(btn_label, use_container_width=True):
            st.session_state.step += 1
            st.rerun()

# ------------------------------------
# 2. 결과 출력 화면
# ------------------------------------
else:
    scores = {"S": 0, "T": 0, "A": 0, "C": 0, "M": 0, "R": 0, "G": 0, "L": 0}
    
    for i, ans_idx in st.session_state.answers.items():
        code = questions[i]["options"][ans_idx][1]
        scores[code] += 1

    pct_S = round((scores["S"] / 5) * 100)
    pct_T = 100 - pct_S
    
    pct_A = round((scores["A"] / 5) * 100)
    pct_C = 100 - pct_A
    
    pct_M = round((scores["M"] / 5) * 100)
    pct_R = 100 - pct_M
    
    pct_G = round((scores["G"] / 5) * 100)
    pct_L = 100 - pct_G

    mbti = ""
    mbti += "S" if scores["S"] >= scores["T"] else "T"
    mbti += "A" if scores["A"] >= scores["C"] else "C"
    mbti += "M" if scores["M"] >= scores["R"] else "R"
    mbti += "G" if scores["G"] >= scores["L"] else "L"

    result_data = TYPE_INFO.get(mbti, TYPE_INFO["SAMG"])

    st.balloons()
    
    st.markdown("### 🎯 당신의 전공 유형은:")
    st.markdown(f'<div class="result-title">✨ {result_data["title"]} ({mbti})</div>', unsafe_allow_html=True)
    
    possible_names = [f"{mbti}.png", f"{mbti}.PNG", f"{mbti}.jpg", f"{mbti}.JPG"]
    img_found = False

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        for name in possible_names:
            if os.path.exists(name):
                st.image(name, use_container_width=True)
                img_found = True
                break
            elif os.path.exists(f"images/{name}"):
                st.image(f"images/{name}", use_container_width=True)
                img_found = True
                break

    if not img_found:
        st.warning(f"⚠️ `{mbti}.png` 이미지를 찾을 수 없습니다.")

    st.info(result_data["desc"])

    st.markdown("---")
    st.subheader("📊 4개 영역별 성향 지표")
    st.caption("선택하신 답변을 바탕으로 한 영역별 비율입니다.")

    def render_indicator(left_text, left_pct, right_text, right_pct):
        st.markdown(f"""
        <div class="indicator-row">
            <span class="indicator-left">{left_text}: {left_pct}%</span>
            <span class="indicator-right">{right_text}: {right_pct}%</span>
        </div>
        """, unsafe_allow_html=True)
        st.progress(left_pct / 100)

    render_indicator("사회/인간 (S)", pct_S, "기술/자연 (T)", pct_T)
    render_indicator("분석/논리 (A)", pct_A, "창의/응용 (C)", pct_C)
    render_indicator("경영/시스템 (M)", pct_M, "연구/자연 (R)", pct_R)
    render_indicator("글로벌/공공 (G)", pct_G, "전문/기술 (L)", pct_L)

    st.markdown("---")
    st.markdown("### 📚 추천 전공 트랙 (제주대학교 자유전공 진입 가능 학과)")
    for dept in result_data["depts"]:
        st.markdown(f"- **{dept}**")

    # 📌 요청사항 2: ** 깨짐 없이 완벽하게 볼드 처리된 안내 박스
    st.markdown("""
    <div style="background-color: #d1e7dd; color: #0f5132; padding: 16px; border-radius: 8px; margin: 16px 0;">
        💡 <b>글로벌자율학부(자유전공)의 특별함!</b><br>
        지금 나온 결과가 마음에 들거나, 혹은 여러 학과 사이에서 고민되나요?<br>
        <b>글로벌자율학부(자유전공)</b>에 입학하면 <b>1학년 동안 이 학과들의 수업을 들어보고</b> 나에게 정말 맞는 전공을 2학년 때 자유롭게 선택할 수 있습니다!
    </div>
    """, unsafe_allow_html=True)

    st.caption("⚠️ **본 테스트는 전공 탐색을 위한 참고용으로만 활용해 주시기 바랍니다.**")

    st.write("")
    if st.button("🔄 테스트 다시 하기", use_container_width=True):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()

    # 📌 요청사항 3: 실제 사용자가 지정한 정확한 링크 반영
    st.markdown("---")
    st.markdown("### 🔗 제주대학교 관련 링크")
    
    col_link1, col_link2 = st.columns(2)
    with col_link1:
        st.link_button("📸 2026 자유전공 인스타그램", "https://www.instagram.com/jnu_start_2026?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==", use_container_width=True)
        st.link_button("🏫 제주대학교 자유전공 홈페이지", "https://openmajor.jejunu.ac.kr/free/index.htm", use_container_width=True)
    with col_link2:
        st.link_button("🎓 제주대학교 입학처", "https://ibsi.jejunu.ac.kr/main", use_container_width=True)
        st.link_button("🏛️ 제주대학교 단과대학 안내", "https://www.jejunu.ac.kr/college/info", use_container_width=True)
