import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_legal_consultation_email(to_email, consultation_topic, report_content):
    """
    AI 법률 상담 내용을 이메일로 전송해주는 함수
    """
    # 이메일 제목 수정 (주식 -> 법률 상담)
    subject = f"⚖️ [{consultation_topic}] AI 법률 상담 결과 안내"
    
    # 줄바꿈 문자를 HTML 태그로 변환
    formatted_content = report_content.replace('\n', '<br>')
    
    # 이메일 본문 HTML 구성
    html_content = f"""
    <html>
    <body style="font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; line-height: 1.6;">
        <h2 style="color: #2c3e50;">⚖️ {consultation_topic} - 법률 상담 요약 리포트</h2>
        <div style="background-color: #f8f9fa; padding: 25px; border-radius: 8px; border: 1px solid #e9ecef;">
            {formatted_content}
        </div>
        <div style="margin-top: 25px; padding-top: 15px; border-top: 1px dashed #ccc;">
            <p style="font-size: 12px; color: #e74c3c; font-weight: bold; margin-bottom: 5px;">
                ※ 주의 및 안내사항
            </p>
            <p style="font-size: 12px; color: #7f8c8d; margin-top: 0;">
                본 리포트는 AI가 제공하는 참고용 법률 정보이며, 실제 법적 효력을 갖는 전문 변호사의 자문을 대체할 수 없습니다.<br>
                정확한 법리적 판단과 중요한 법적 결정은 반드시 법률 전문가(변호사)와 직접 상담하시기 바랍니다.
            </p>
        </div>
    </body>
    </html>
    """

    print(f"[이메일 전송 요청] 수신: {to_email}")
    
    try:
        # SMTP 설정 가져오기
        host = os.getenv("SMTP_HOST")
        port = int(os.getenv("SMTP_PORT", 587))
        user = os.getenv("SMTP_USER")
        password = os.getenv("SMTP_PASSWORD")

        if not all([host, user, password]):
            return {"success": False, "error": "SMTP 설정이 누락되었습니다. (.env 파일을 확인하세요)"}

        # 메시지 생성
        msg = MIMEText(html_content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = user
        msg['To'] = to_email

        # 서버 연결 및 전송
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
            
        print("[이메일 전송 성공!]")
        return {"success": True, "message": "상담 내용이 성공적으로 발송되었습니다."}
        
    except Exception as e:
        print(f"[이메일 전송 실패]: {str(e)}")
        return {"success": False, "error": str(e)}