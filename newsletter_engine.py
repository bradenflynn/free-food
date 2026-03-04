import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email Configuration (User needs to fill these in .env)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

DATA_FILE = "data.json"

def get_haul_html(events):
    """Generates a Brutalist/VÉLOCE style HTML email."""
    confirmed = [e for e in events if e.get('has_free_food')]
    if not confirmed:
        return None

    items_html = ""
    for event in confirmed:
        items_html += f"""
        <div style="border: 3px solid #000; margin-bottom: 20px; padding: 20px; background: #fff;">
            <h2 style="font-family: 'Impact', sans-serif; text-transform: uppercase; font-size: 24px; margin: 0;">{event.get('club_name', 'STUDENT ORG')}</h2>
            <p style="font-weight: bold; margin: 10px 0;">📍 {event.get('location', 'USD')}</p>
            <p style="font-weight: bold; margin: 5px 0;">🕒 {event.get('date', '')} | {event.get('time', '')}</p>
            <div style="background: #C19A6B; border: 2px solid #000; padding: 10px; margin-top: 10px; font-weight: 900;">
                🍕 {event.get('food_provided', 'FREE FOOD')}
            </div>
        </div>
        """

    return f"""
    <html>
    <body style="font-family: sans-serif; background: #C19A6B; padding: 40px 20px; color: #000;">
        <div style="max-width: 600px; margin: 0 auto; background: #fff; border: 4px solid #000; padding: 30px;">
            <h1 style="font-family: 'Impact', sans-serif; font-size: 48px; text-transform: uppercase; margin: 0 0 20px 0; border-bottom: 4px solid #000;">THE FREE LUNCH</h1>
            <p style="font-size: 18px; font-weight: bold; margin-bottom: 30px;">YOUR DAILY HAUL IS READY. ACT FAST.</p>
            
            {items_html}
            
            <div style="margin-top: 40px; border-top: 4px solid #000; padding-top: 20px; text-align: center;">
                <p style="font-weight: 900;">VÉLOCE PREMIER AGGREGATION</p>
                <p style="font-size: 12px;">You are receiving this because you are part of the USD Inner Circle.</p>
            </div>
        </div>
    </body>
    </html>
    """

def send_daily_haul(to_email):
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r") as f:
        events = json.load(f)

    html_content = get_haul_html(events)
    if not html_content:
        print("No free food today. Skipping email.")
        return

    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = f"🍕 THE HAUL: {datetime.now().strftime('%b %d')} | {len([e for e in events if e.get('has_free_food')])} Items Found"

    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print(f"✅ Success: Haul sent to {to_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

if __name__ == "__main__":
    # For testing, we send to the FROM_EMAIL or a test address
    test_recipient = os.getenv("TEST_EMAIL", FROM_EMAIL)
    if test_recipient:
        send_daily_haul(test_recipient)
    else:
        print("Set TEST_EMAIL in your .env to test the newsletter.")
