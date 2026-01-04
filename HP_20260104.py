import streamlit as st
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- [1] 페이지 기본 설정 ---
st.set_page_config(
    page_title="Solventics AI Inc.",
    page_icon="🤖",
    layout="wide"
)

# --- [2] 구글 시트 연동 함수 (새로 추가된 부분) ---
def save_to_sheet(name, email, message):
    """
    사용자가 입력한 문의 내용을 구글 스프레드시트에 저장하는 함수
    """
    try:
        # 1. 인증 범위 설정
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        
        # 2. secrets.toml에서 인증 정보 가져오기
        # 주의: .streamlit/secrets.toml 파일이 반드시 있어야 합니다.
        creds_dict = st.secrets["gcp_service_account"]
        
        # 3. 인증 자격 증명 생성 및 클라이언트 연결
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # 4. 스프레드시트 열기 (시트 이름: Contact_Data)
        sheet = client.open("Contact_Data").sheet1  
        
        # 5. 데이터 추가 (현재시간, 이름, 이메일, 내용)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, name, email, message])
        
        return True # 저장 성공
        
    except Exception as e:
        # 에러가 나면 화면에 이유를 출력해 줌 (디버깅용)
        st.error(f"데이터 저장 중 오류가 발생했습니다: {e}")
        return False # 저장 실패

# --- [3] 사이드바 (네비게이션) ---
st.sidebar.title("Solventics AI Inc.")
page = st.sidebar.radio("Menu", ["Home", "About Us", "Solutions", "Contact"])

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

# 2. About Us 페이지
elif page == "About Us":
    st.title("About Solventics AI")
    st.write("### '문제(Problem)를 녹여내는(Solvent) AI 솔루션'")
    st.write("""
    Solventics AI Inc.는 고도의 통계적 지식과 IT 기술을 바탕으로 설립된 법인입니다.
    금융, 보험, 제조 등 다양한 산업 분야에서 데이터가 가진 잠재력을 극대화하며,
    실질적인 비즈니스 임팩트를 창출하는 것을 목표로 합니다.
    """)
    
    st.markdown("---")
    st.write("#### 👨‍💼 Leadership")
    st.write("**CEO / Ph.D. in Statistics**")
    st.caption("통계학 박사 학위 및 글로벌 컨설팅 경험 보유")

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
        st.write("- **Integrated LNMR Analyzer:** 보험 리스크 분석 및 자동 리포팅 솔루션")
        st.write("- 금융 시장 예측 및 포트폴리오 최적화 도구")

# 4. Contact 페이지 (기능 업그레이드됨)
elif page == "Contact":
    st.title("Contact Us")
    st.write("Solventics AI와 함께 비즈니스의 미래를 설계하세요.")
    
    with st.form("contact_form"):
        name = st.text_input("이름 (Name)")
        email = st.text_input("이메일 (Email)")
        message = st.text_area("문의 내용 (Message)")
        
        submitted = st.form_submit_button("전송하기")
        
        if submitted:
            # 빈칸 검사
            if not name or not email or not message:
                st.warning("이름, 이메일, 내용을 모두 입력해 주세요.")
            else:
                # 로딩 표시 (UX 향상)
                with st.spinner("문의 내용을 전송 중입니다..."):
                    # 구글 시트 저장 함수 호출
                    success = save_to_sheet(name, email, message)
                    
                    if success:
                        st.success(f"✅ {name}님, 문의가 성공적으로 접수되었습니다! 담당자가 검토 후 {email}로 연락드리겠습니다.")
                    else:
                        st.error("서버 연결 문제로 전송에 실패했습니다. 잠시 후 다시 시도해 주세요.")

    st.markdown("---")
    st.write("📍 **Office:** (06025) 서울특별시 강남구 논현로 152길 15 311호")
    st.write("📧 **Email:** contact@solventicsai.com") # 도메인 수정됨

# 푸터
st.markdown("---")
st.caption("© 2026 Solventics AI Inc. All Rights Reserved.")