"""
TEST SCRIPT - Run this to PROVE emails work
This sends a TEST email to ishrakarafneo@gmail.com RIGHT NOW
"""
import asyncio
import os
from dotenv import load_dotenv
from services.email_service import EmailService

async def test_email():
    load_dotenv()
    
    print("=" * 60)
    print("EMAIL TEST - Sending to ishrakarafneo@gmail.com")
    print("=" * 60)
    
    test_logs = [
        {
            "device_id": "TEST_DEVICE_12345",
            "source": "pornhub.com",
            "reason": "Adult Content Detected",
            "context": "URL Monitor Block",
            "timestamp": "2025-11-26T02:00:00"
        },
        {
            "device_id": "TEST_DEVICE_12345",
            "source": "instagram.com/reels",
            "reason": "Dopamine Detox Active",
            "context": "Scroll Blocker",
            "timestamp": "2025-11-26T02:05:00"
        },
        {
            "device_id": "TEST_DEVICE_12345",
            "source": "xhamster.com",
            "reason": "Adult Content Detected",
            "context": "URL Monitor Block",
            "timestamp": "2025-11-26T02:10:00"
        }
    ]
    
    email_service = EmailService()
    
    if not email_service.is_configured():
        print("\n❌ EMAIL NOT CONFIGURED!")
        print("\nYou need to set ONE of these in your .env file:")
        print("\nOption 1: SendGrid")
        print("  SENDGRID_API_KEY=SG....")
        print("\nOption 2: Gmail SMTP")
        print("  SMTP_HOST=smtp.gmail.com")
        print("  SMTP_PORT=587")
        print("  SMTP_USERNAME=ishrakarafneo@gmail.com")
        print("  SMTP_PASSWORD=your_app_password")
        print("\nGet Gmail app password: https://myaccount.google.com/apppasswords")
        return
    
    print("\n✅ Email is configured!")
    print(f"📧 Will send to: {email_service.admin_email}")
    
    print("\n📨 Sending test forensic report...")
    try:
        await email_service.send_research_report(
            logs=test_logs,
            device_id="TEST_DEVICE_12345"
        )
        print("\n✅ SUCCESS! Email sent!")
        print(f"📬 Check {email_service.admin_email} inbox (including spam folder)")
        print("\n📄 Email includes:")
        print("  - HTML formatted report")
        print("  - PDF attachment with full forensic analysis")
        if email_service.openai_key:
            print("  - GPT-4 AI behavioral analysis")
        else:
            print("  - Statistical heuristic analysis (add OPENAI_API_KEY for GPT-4)")
            
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        print("\nTroubleshooting:")
        print("1. Check your .env file has correct credentials")
        print("2. For Gmail: Enable 2-Step Verification and create App Password")
        print("3. For SendGrid: Verify API key has 'Mail Send' permission")

if __name__ == "__main__":
    asyncio.run(test_email())
