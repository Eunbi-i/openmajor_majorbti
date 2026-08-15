# ------------------------------------
# 0. 시작 안내 화면 (커버 페이지)
# ------------------------------------
if st.session_state.step == -1:
    st.markdown(
        '<div class="header-sub1">제주대학교 전공체험의 날 - 글로벌자율학부 자유전공 체험</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="custom-title">🎓 전공탐색 MBTI TEST</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="header-sub2">개인 맞춤형 전공 탐색 및 추천 프로그램 | 총 20문항</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr style="margin: 8px 0 16px 0;">', unsafe_allow_html=True)

    cover_img_path = "main_cover.png"
    if os.path.exists(cover_img_path):
        with open(cover_img_path, "rb") as f:
            encoded_img = base64.b64encode(f.read()).decode()
        ext = cover_img_path.split(".")[-1].lower()
        mime_type = "image/png" if ext == "png" else "image/jpeg"

        st.markdown(
            f"""
            <div class="cover-img-container">
                <img src="data:{mime_type};base64,{encoded_img}" alt="메인 캐릭터">
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 👇 자유전공 진입 가능 학과 탐색 목적에 맞춰 안내 문구 수정
    st.markdown(
        """
        <div class="start-container">
            <h2>나에게 딱 맞는 전공은 무엇일까?</h2>
            <p>간단한 20개 질문을 통해 나의 적성과 성향을 분석하고,<br>
            <b>제주대학교 자유전공 입학 후 진입 가능한 추천 학과 트랙</b>을 확인해 보세요!</p>
            <p style="font-size: 13px; color: #64748B; margin-top: 12px;">⏱️ 소요 시간: 약 2~3분</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🚀 테스트 시작하기", use_container_width=True, type="primary"):
        st.session_state.step = 0
        st.rerun()
