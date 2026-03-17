import streamlit as st
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone, timedelta

# --- [1] 페이지 기본 설정 ---
st.set_page_config(
    page_title="Solventics AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- [2] 언어 설정 (기본값: 한국어) ---
if "lang" not in st.session_state:
    st.session_state.lang = "한국어"

# --- [3] 텍스트 딕셔너리 ---
TEXT = {
    "한국어": {
        "site_title": "Solventics AI",
        "menu_label": "메뉴",
        "menu_items": ["홈", "회사 소개", "솔루션", "공지사항", "문의하기"],
        "sidebar_caption": "중요한 것에 집중하세요.\n리스크는 저희가 처리합니다.",

        # Home
        "home_title": "데이터 기반 의사결정, AI가 이끄는 미래",
        "home_subtitle": "Solventics AI에 오신 것을 환영합니다.",
        "home_vision_label": "💡 **Our Vision**",
        "home_vision_text": """
        복잡한 데이터를 명쾌한 솔루션으로 전환합니다.
        \n최신 인공지능 기술과 통계적 방법론을 결합하여 비즈니스의 불확실성을 해결합니다.
        """,
        "home_value_label": "🚀 **Core Value**",
        "home_value_text": """
        - **Precision:** 정밀한 데이터 분석
        - **Innovation:** 혁신적인 AI 모델링
        - **Integrity:** 신뢰할 수 있는 결과
        """,
        "home_news_title": "📢 최신 소식",
        "news_items": [
            ("2026.01.09", "Solventics AI Risk Pro 개발 (Pre-alpha)"),
            ("2026.01.06", "Solventics AI 법인 홈페이지 정식 오픈"),
            ("2026.01.02", "AI Actuarial Consultant Pro 개발 (Beta)"),
            ("2025.12.30", "법인 설립 등기 완료"),
        ],

        # About us
        "about_title": "회사 소개",
        "about_tagline": "### '문제(Problem)를 녹여내는(Solvent) AI 솔루션'",
        "about_desc": """
        Solventics AI Inc.는 고도의 통계적 지식과 IT 기술을 바탕으로 설립된 법인입니다.
        \n금융, 보험, 제조 등 다양한 산업 분야에서 데이터가 가진 잠재력을 극대화하며,
        실질적인 비즈니스 임팩트를 창출하는 것을 목표로 합니다.
        """,
        "leadership_title": "리더십",
        "ceo_name": "**한승진 (Paul) (Ph.D.)**",
        "ceo_title": "창업자 & 대표이사 (CEO)",
        "ceo_quote": "**\"데이터 속에 숨겨진 리스크와 기회를 통계적 통찰로 밝혀냅니다.\"**",
        "ceo_bio": """
        - **통계학 박사 (Ph.D. in Statistics)**
        - 현) 보험 계리 및 리스크 관리(Actuarial Science & Risk Mgmt) 전문 기업 Solventics AI 대표
        - 데이터 기반 의사결정 및 기업 전략 수립 전문가
        - 16년 이상의 컨설팅, 세일즈 및 지역 경영(Regional Management) 경력
        """,

        # Solutions
        "solutions_title": "솔루션",
        "tab_consulting": "AI 컨설팅",
        "tab_saas": "SaaS 제품",
        "consulting_title": "🏢 AI & 데이터 컨설팅",
        "consulting_items": [
            "기업 맞춤형 데이터 분석 전략 수립",
            "리스크 관리 및 예측 모델링",
            "프로세스 자동화 (RPA) 구축",
        ],
        "saas_title": "💻 특화 소프트웨어",
        "saas_items": [
            "**Solventics AI Risk Pro (Pre-alpha):** 보험 리스크 분석 및 자동 리포팅 솔루션",
            "**AI Actuarial Consultant Pro (Beta):** Mortality Risk 심층 분석 및 진단 솔루션",
            "금융 시장 예측 및 포트폴리오 최적화 도구",
        ],

        # Notice
        "notice_title": "공지사항 & 뉴스",
        "notice_desc": "Solventics AI의 새로운 소식과 공지사항을 알려드립니다.",
        "notices": [
            {"date": "2026-01-06", "title": "Solventics AI 공식 홈페이지 오픈", "tag": "뉴스"},
            {"date": "2025-12-30", "title": "주식회사 솔벤틱스에이아이 설립 완료", "tag": "회사"},
        ],

        # Contact
        "contact_title": "문의하기",
        "contact_desc": "Solventics AI와 함께 비즈니스의 미래를 설계하세요.",
        "form_name": "이름 (Name)",
        "form_email": "이메일 (Email)",
        "form_message": "문의 내용 (Message)",
        "form_submit": "전송하기",
        "form_warn": "이름, 이메일, 내용을 모두 입력해 주세요.",
        "form_sending": "문의 내용을 전송 중입니다...",
        "form_success": "님, 문의가 성공적으로 접수되었습니다! 담당자가 검토 후 연락드리겠습니다.",
        "form_error": "서버 연결 문제로 전송에 실패했습니다.",
        "office_label": "📍 **주소:**",
        "office_value": "(06025) 서울특별시 강남구 논현로 152길 15 311호",
        "email_label": "📧 **이메일:**",

        "footer": "© 2026 Solventics AI Inc. All Rights Reserved.",
    },

    "English": {
        "site_title": "Solventics AI",
        "menu_label": "Menu",
        "menu_items": ["Home", "About us", "Solutions", "Notice", "Contact"],
        "sidebar_caption": "Focus on what matters.\nWe handle the risk.",

        # Home
        "home_title": "Data-Driven Decisions, AI-Powered Future",
        "home_subtitle": "Welcome to Solventics AI.",
        "home_vision_label": "💡 **Our Vision**",
        "home_vision_text": """
        We transform complex data into clear, actionable solutions.
        \nWe combine cutting-edge artificial intelligence with rigorous statistical methodology to eliminate business uncertainty.
        """,
        "home_value_label": "🚀 **Core Value**",
        "home_value_text": """
        - **Precision:** Accurate, reliable data analysis
        - **Innovation:** State-of-the-art AI modeling
        - **Integrity:** Results you can trust
        """,
        "home_news_title": "📢 Latest News",
        "news_items": [
            ("2026.01.09", "Solventics AI Risk Pro under development (Pre-alpha)"),
            ("2026.01.06", "Solventics AI official website launched"),
            ("2026.01.02", "AI Actuarial Consultant Pro under development (Beta)"),
            ("2025.12.30", "Company incorporation completed"),
        ],

        # About us
        "about_title": "About Solventics AI",
        "about_tagline": "### 'AI Solutions that Dissolve Problems'",
        "about_desc": """
        Solventics AI Inc. was founded on a foundation of advanced statistical expertise and IT technology.
        \nOur mission is to maximize the potential hidden in data across diverse industries —
        including finance, insurance, and manufacturing — and to generate tangible business impact.
        """,
        "leadership_title": "Leadership",
        "ceo_name": "**Seungjin Han (Paul), Ph.D.**",
        "ceo_title": "Founder & Chief Executive Officer",
        "ceo_quote": "**\"We uncover the risks and opportunities hidden in data through statistical insight.\"**",
        "ceo_bio": """
        - **Ph.D. in Statistics**
        - CEO of Solventics AI, specializing in Actuarial Science & Risk Management
        - Expert in data-driven decision-making and corporate strategy
        - 16+ years of experience in consulting, sales, and regional management
        """,

        # Solutions
        "solutions_title": "Our Solutions",
        "tab_consulting": "AI Consulting",
        "tab_saas": "SaaS Products",
        "consulting_title": "🏢 AI & Data Consulting",
        "consulting_items": [
            "Custom data analytics strategy for enterprises",
            "Risk management and predictive modeling",
            "Robotic Process Automation (RPA) implementation",
        ],
        "saas_title": "💻 Specialized Software",
        "saas_items": [
            "**Solventics AI Risk Pro (Pre-alpha):** Insurance risk analysis and automated reporting solution",
            "**AI Actuarial Consultant Pro (Beta):** In-depth mortality risk analysis and diagnostics",
            "Financial market forecasting and portfolio optimization tools",
        ],

        # Notice
        "notice_title": "Notice & News",
        "notice_desc": "Stay up to date with the latest news and announcements from Solventics AI.",
        "notices": [
            {"date": "2026-01-06", "title": "Solventics AI Official Website Launched", "tag": "News"},
            {"date": "2025-12-30", "title": "Solventics AI Inc. Incorporation Completed", "tag": "Company"},
        ],

        # Contact
        "contact_title": "Contact Us",
        "contact_desc": "Let's design the future of your business together with Solventics AI.",
        "form_name": "Name",
        "form_email": "Email",
        "form_message": "Message",
        "form_submit": "Send Message",
        "form_warn": "Please fill in your name, email, and message.",
        "form_sending": "Sending your message...",
        "form_success": ", your message has been received! We will get back to you shortly.",
        "form_error": "Submission failed due to a server connection issue.",
        "office_label": "📍 **Office:**",
        "office_value": "311, 15, Nonhyeon-ro 152-gil, Gangnam-gu, Seoul, Korea (06025)",
        "email_label": "📧 **Email:**",

        "footer": "© 2026 Solventics AI Inc. All Rights Reserved.",
    },
}

# --- [4] 구글 시트 연동 함수 ---

def get_gspread_client():
    """공통 gspread 클라이언트 반환"""
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def save_to_sheet(name, email, message):
    try:
        if "gcp_service_account" not in st.secrets:
            st.error("Secrets 설정을 찾을 수 없습니다.")
            return False
        client = get_gspread_client()
        sheet = client.open("Contact_Data").sheet1
        KST = timezone(timedelta(hours=9))
        timestamp = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, name, email, message])
        return True
    except Exception as e:
        st.error(f"데이터 저장 중 오류가 발생했습니다: {e}")
        return False

@st.cache_data(ttl=300)  # 5분 캐시 (홈페이지 성능 유지)
def load_notices():
    """
    Google Sheets 'Notice_Data' 시트에서 공지사항을 불러옵니다.
    컬럼 순서: date | title_ko | title_en | tag_ko | tag_en
    시트가 없거나 오류 시 하드코딩된 기본값 반환.
    """
    try:
        if "gcp_service_account" not in st.secrets:
            raise ValueError("No secrets")
        client = get_gspread_client()
        sheet = client.open("Notice_Data").sheet1
        rows = sheet.get_all_records()  # 헤더 행 자동 제외
        return rows  # [{"date":..., "title_ko":..., ...}, ...]
    except Exception:
        # 시트 연결 실패 시 기본 데이터 표시 (안전망)
        return [
            {"date": "2026-01-06", "title_ko": "Solventics AI 공식 홈페이지 오픈",
             "title_en": "Official Website Launched", "tag_ko": "뉴스", "tag_en": "News"},
            {"date": "2025-12-30", "title_ko": "주식회사 솔벤틱스에이아이 설립 완료",
             "title_en": "Incorporation Completed", "tag_ko": "회사", "tag_en": "Company"},
        ]

# --- [5] 사이드바 ---
with st.sidebar:
    st.title("Solventics AI")

    # 언어 선택 토글 (한국어 기본값)
    lang_option = st.radio("🌐 Language / 언어", ["한국어", "English"],
                           index=0 if st.session_state.lang == "한국어" else 1,
                           horizontal=True)
    st.session_state.lang = lang_option
    T = TEXT[st.session_state.lang]

    st.divider()
    page = st.radio(T["menu_label"], T["menu_items"])
    st.divider()
    st.caption(T["sidebar_caption"])

# 현재 언어 텍스트 단축 참조
T = TEXT[st.session_state.lang]
menu = T["menu_items"]

# --- [6] 페이지별 구성 ---

# 1. Home
if page == menu[0]:
    st.title(T["home_title"])
    st.subheader(T["home_subtitle"])
    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.info(T["home_vision_label"])
        st.write(T["home_vision_text"])
    with col2:
        st.success(T["home_value_label"])
        st.write(T["home_value_text"])

    st.divider()
    st.subheader(T["home_news_title"])
    notices = load_notices()
    title_key = "title_ko" if st.session_state.lang == "한국어" else "title_en"
    for row in notices[:4]:  # 홈에는 최신 4개만 표시
        c1, c2 = st.columns([1, 4])
        with c1:
            st.caption(row.get("date", ""))
        with c2:
            st.write(row.get(title_key, ""))

# 2. About us
elif page == menu[1]:
    st.title(T["about_title"])
    st.write(T["about_tagline"])
    st.write(T["about_desc"])
    st.divider()
    st.header(T["leadership_title"])
    l_col1, l_col2 = st.columns([1, 3])
    with l_col1:
        st.markdown("<div style='text-align: center; font-size: 100px;'>👨‍💼</div>", unsafe_allow_html=True)
    with l_col2:
        st.write(T["ceo_name"])
        st.caption(T["ceo_title"])
        st.write(T["ceo_quote"])
        st.write(T["ceo_bio"])

# 3. Solutions
elif page == menu[2]:
    st.title(T["solutions_title"])
    tab1, tab2 = st.tabs([T["tab_consulting"], T["tab_saas"]])
    with tab1:
        st.header(T["consulting_title"])
        for item in T["consulting_items"]:
            st.write(f"- {item}")
    with tab2:
        st.header(T["saas_title"])
        for item in T["saas_items"]:
            st.write(f"- {item}")

# 4. Notice
elif page == menu[3]:
    st.title(T["notice_title"])
    st.write(T["notice_desc"])
    st.markdown("---")
    title_key = "title_ko" if st.session_state.lang == "한국어" else "title_en"
    tag_key   = "tag_ko"   if st.session_state.lang == "한국어" else "tag_en"
    notices = load_notices()
    if notices:
        for notice in notices:
            with st.container():
                col1, col2, col3 = st.columns([1, 4, 1])
                with col1:
                    st.caption(notice.get("date", ""))
                with col2:
                    st.write(f"**{notice.get(title_key, '')}**")
                with col3:
                    st.info(notice.get(tag_key, ""))
                st.markdown("---")
    else:
        st.info("등록된 공지사항이 없습니다." if st.session_state.lang == "한국어" else "No notices available.")

# 5. Contact
elif page == menu[4]:
    st.title(T["contact_title"])
    st.write(T["contact_desc"])
    with st.form("contact_form"):
        name = st.text_input(T["form_name"])
        email = st.text_input(T["form_email"])
        message = st.text_area(T["form_message"])
        submitted = st.form_submit_button(T["form_submit"])
        if submitted:
            if not name or not email or not message:
                st.warning(T["form_warn"])
            else:
                with st.spinner(T["form_sending"]):
                    success = save_to_sheet(name, email, message)
                    if success:
                        st.success(f"✅ {name}{T['form_success']}")
                    else:
                        st.error(T["form_error"])
    st.markdown("---")
    st.write(f"{T['office_label']} {T['office_value']}")
    st.write(f"{T['email_label']} contact@solventicsai.com")

# 푸터
st.markdown("---")
st.caption(T["footer"])
