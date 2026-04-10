import time
import streamlit as st
from test_langgraph import build_graph
from email_utils import send_legal_consultation_email

# 웹 페이지 탭 설정
st.set_page_config(page_title="AI 법률 상담", page_icon="⚖️", layout="centered")

@st.cache_resource
def load_graph():
    return build_graph()

graph = load_graph()

st.title("⚖️ AI 법률 상담 서비스")
st.markdown("질문을 입력하시면 AI가 관련 법률과 판례를 바탕으로 답변해 드립니다.")
st.markdown("---")

# 1. 사용자 질문 입력
query = st.text_area("법률 관련 고민을 상세히 적어주세요.", height=100, placeholder="예: 음주운전으로 적발되었는데 처벌 수위가 어떻게 되나요?")

# 2. 상담 결과 생성 (버튼 클릭 시 처리 후 session_state에 저장만 함)
if st.button("상담 결과 확인하기", type="primary"):
    if not query.strip():
        st.warning("질문을 입력해 주세요.")
    else:
        with st.spinner("관련 법령과 판례를 분석하는 중입니다..."):
            t0 = time.perf_counter()
            result = graph.invoke({"user_query": query})
            dt = (time.perf_counter() - t0) * 1000
            
            # 화면이 새로고침되어도 날아가지 않도록 메모리에 결과 저장
            st.session_state['query'] = query
            st.session_state['result'] = result
            st.session_state['time'] = dt

# =====================================================================
# 3. 결과 화면 출력 (저장된 결과가 있을 때만 화면에 렌더링)
# =====================================================================
if 'result' in st.session_state:
    saved_query = st.session_state['query']
    saved_result = st.session_state['result']
    saved_time = st.session_state['time']

    st.success(f"분석 완료! (처리시간: {saved_time:.1f}ms)")

    # 사용자가 보기 편하도록 핵심 답변과 판례를 먼저 배치
    st.write("### 💡 AI 법률 상담 결과")
    st.info(saved_result.get("answer"))

    # st.write("### 📚 관련 판례 및 법령")
    # st.success(saved_result.get("matched_docs"))

    # 기술적인 분류 정보는 접어두기(Expander)로 숨겨서 UI를 깔끔하게 처리
    with st.expander("세부 분류 정보 보기"):
        st.write(f"**분류 분야:** {saved_result.get('query_category')} (신뢰도: {saved_result.get('confidence')})")
        st.write(f"**분류 근거:** {saved_result.get('reasoning')}")

    st.markdown("---")

    # =====================================================================
    # 4. 이메일 전송 섹션 (결과 확인 후 선택 사항)
    # =====================================================================
    st.write("#### 📧 상담 결과 이메일로 보관하기 (선택)")
    
    # st.form을 사용하여 이메일 입력 중 화면이 깜빡이는 현상 방지
    with st.form("email_form", clear_on_submit=False):
        email_input = st.text_input("받으실 이메일 주소를 입력하세요.", placeholder="example@email.com")
        submit_email = st.form_submit_button("결과 메일로 받기")
        
        if submit_email:
            if not email_input.strip():
                st.warning("이메일 주소를 입력해주세요.")
            else:
                with st.spinner("이메일을 전송 중입니다..."):
                    topic_preview = saved_query[:15] + "..." if len(saved_query) > 15 else saved_query
                    
                    report_content = f"""
                    <strong>[사용자 질문]</strong><br>{saved_query}<br><br>
                    <strong>[분야 분류]</strong> {saved_result.get('query_category')} (신뢰도: {saved_result.get('confidence')})<br>
                    <strong>[관련 판례]</strong><br>{saved_result.get('matched_docs')}<br><br>
                    <strong>[AI 상세 응답]</strong><br>{saved_result.get('answer')}
                    """
                    
                    email_response = send_legal_consultation_email(
                        to_email=email_input.strip(),
                        consultation_topic=topic_preview,
                        report_content=report_content
                    )
                    
                    if email_response["success"]:
                        st.success("✅ 메일이 성공적으로 전송되었습니다! 이메일함을 확인해 주세요.")
                    else:
                        st.error(f"❌ 전송 실패: {email_response['error']}")