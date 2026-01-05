import streamlit as st
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- [1] 페이지 기본 설정 ---
st.set_page_config(
    page_title="Solventics AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"  # 이 옵션 추가
)

# 스타일 숨기기 (Streamlit 기본 메뉴 등)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- [2] 구글 시트 연동 함수 (기존 유지) ---
def save_to_sheet(name, email, message):
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        # secrets.toml 파일이 있어야 작동합니다. 없으면 로컬 에러 방지를 위해 예외처리 필요
        if "gcp_service_account" in st.secrets:
            creds_dict = st.secrets["gcp_service_account"]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)
            sheet = client.open("Contact_Data").sheet1  
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([timestamp, name, email, message])
            return True
        else:
            st.error("Secrets 설정을 찾을 수 없습니다.")
            return False
    except Exception as e:
        st.error(f"데이터 저장 중 오류가 발생했습니다: {e}")
        return False

# --- [3] 사이드바 (네비게이션) ---
with st.sidebar:
    st.title("Solventics AI")
    # About Us -> About us 로 변경, Notice 추가
    page = st.radio("Menu", ["Home", "About us", "Solutions", "Notice", "Contact"])
    
    st.divider()
    st.caption("Focus on what matters.\nWe handle the risk.")

# --- [4] 페이지별 구성 ---

# 1. Home 페이지
if page == "Home":
    st.title("Data-Driven Decisions, AI-Powered Future")
    st.subheader("Solventics AI에 오신 것을 환영합니다.")
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info("💡 **Our Vision**")
        st.write("""
        복잡한 데이터를 명쾌한 솔루션으로 전환합니다.
        Solventics AI는 최신 인공지능 기술과 통계적 방법론을 결합하여
        비즈니스의 불확실성을 해결합니다.
        """)
        
    with col2:
        st.success("🚀 **Core Value**")
        st.write("""
        - **Precision:** 정밀한 데이터 분석
        - **Innovation:** 혁신적인 AI 모델링
        - **Integrity:** 신뢰할 수 있는 결과
        """)
    
    # [NEW] 하단 공지사항 요약 섹션 추가
    st.divider()
    st.subheader("📢 Latest News")
    
    news_col1, news_col2 = st.columns([1, 4])
    with news_col1:
        st.caption("2026.01.09")
    with news_col2:
        st.write("Solventics AI Risk Pro 개발 (Pre-alpha)")

    news_col1, news_col2 = st.columns([1, 4])
    with news_col1:
        st.caption("2026.01.06")
    with news_col2:
        st.write("Solventics AI 법인 홈페이지 정식 오픈")

    news_col1, news_col2 = st.columns([1, 4])
    with news_col1:
        st.caption("2026.01.02")
    with news_col2:
        st.write("AI Actuarial Consultant Pro 개발 (Beta)")

    news_col1, news_col2 = st.columns([1, 4])
    with news_col1:
        st.caption("2025.12.30")
    with news_col2:
        st.write("법인 설립 등기 완료")

# 2. About us 페이지 (수정됨)
elif page == "About us":
    st.title("About Solventics AI")
    st.write("### '문제(Problem)를 녹여내는(Solvent) AI 솔루션'")
    st.write("""
    Solventics AI Inc.는 고도의 통계적 지식과 IT 기술을 바탕으로 설립된 법인입니다.
    금융, 보험, 제조 등 다양한 산업 분야에서 데이터가 가진 잠재력을 극대화하며,
    실질적인 비즈니스 임팩트를 창출하는 것을 목표로 합니다.
    """)
    
    st.divider()
    
    # [NEW] Leadership 섹션 강화
    st.header("Leadership")
    
    l_col1, l_col2 = st.columns([1, 3])
    
    with l_col1:
        # 프로필 이미지가 있다면 st.image("profile.jpg") 사용
        st.markdown("<div style='text-align: center; font-size: 100px;'>👨‍💼</div>", unsafe_allow_html=True)
        
    with l_col2:
        # 🔴 [중요] 아래 이름을 실제 대표님 성함으로 바꿔주세요
        st.write("**한승진 (Paul) (Ph.D.)**") 
        st.caption("Founder & Chief Executive Officer")
        
        st.write("""
        **"데이터 속에 숨겨진 리스크와 기회를 통계적 통찰로 밝혀냅니다."**
        
        - **Ph.D. in Statistics** (통계학 박사)
        - 현) 보험 계리 및 리스크 관리(Actuarial Science & Risk Mgmt) 전문 기업 Solventics AI 대표
        - 데이터 기반 의사결정 및 기업 전략 수립 전문가
        - 10년 이상의 컨설팅, 세일즈 및 지역 경영(Regional Management) 경력
        """)

# 3. Solutions 페이지
elif page == "Solutions":
    st.title("Our Solutions")
    
    tab1, tab2 = st.tabs(["AI Consulting", "SaaS Products"])
    
    with tab1:
        st.header("🏢 AI & Data Consulting")
        st.write("- 기업 맞춤형 데이터 분석 전략 수립")
        st.write("- 리스크 관리 및 예측 모델링")
        st.write("- 프로세스 자동화 (RPA) 구축")
        
    with tab2:
        st.header("💻 Specialized Software")
        st.write("- **Solventics AI Risk Pro (Pre-alpha):** 보험 리스크 분석 및 자동 리포팅 솔루션")
        st.write("- **AI Actuarial Consultant Pro (Beta):** Mortality Risk 심층 분석 및 진단 솔루션")
        st.write("- 금융 시장 예측 및 포트폴리오 최적화 도구")

# [NEW] 4. Notice 페이지 (메뉴에 추가됨)
elif page == "Notice":
    st.title("Notice & News")
    st.write("Solventics AI의 새로운 소식과 공지사항을 알려드립니다.")
    st.markdown("---")
    
    # 공지사항 리스트 형태
    notices = [
        {"date": "2026-01-06", "title": "Solventics AI 공식 홈페이지 오픈", "tag": "News"},
        {"date": "2025-12-30", "title": "주식회사 솔벤틱스에이아이 설립 완료", "tag": "Company"},        
    ]

    for notice in notices:
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.caption(notice["date"])
            with col2:
                st.write(f"**{notice['title']}**")
            with col3:
                st.info(notice['tag'])
            st.markdown("---")

# 5. Contact 페이지
elif page == "Contact":
    st.title("Contact Us")
    st.write("Solventics AI와 함께 비즈니스의 미래를 설계하세요.")
    
    with st.form("contact_form"):
        name = st.text_input("이름 (Name)")
        email = st.text_input("이메일 (Email)")
        message = st.text_area("문의 내용 (Message)")
        
        submitted = st.form_submit_button("전송하기")
        
        if submitted:
            if not name or not email or not message:
                st.warning("이름, 이메일, 내용을 모두 입력해 주세요.")
            else:
                with st.spinner("문의 내용을 전송 중입니다..."):
                    success = save_to_sheet(name, email, message)
                    if success:
                        st.success(f"✅ {name}님, 문의가 성공적으로 접수되었습니다! 담당자가 검토 후 {email}로 연락드리겠습니다.")
                    else:
                        st.error("서버 연결 문제로 전송에 실패했습니다.")

    st.markdown("---")
    st.write("📍 **Office:** (06025) 서울특별시 강남구 논현로 152길 15 311호")
    st.write("📧 **Email:** contact@solventicsai.com") # 도메인 닷컴->ai로 통일

# 푸터
st.markdown("---")
st.caption("© 2026 Solventics AI Inc. All Rights Reserved.")