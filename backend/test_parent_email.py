"""
Test Gmail SMTP Configuration
Verifies that parent alerts can be sent via Gmail
"""

import os
import sys
from dotenv import load_dotenv
import asyncio

# Load environment
load_dotenv()

async def test_gmail_smtp():
    """Test Gmail SMTP configuration"""
    print("=" * 70)
    print("GMAIL SMTP CONFIGURATION TEST")
    print("=" * 70)
    print()
    
    # Check configuration
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    email_sender = os.getenv("EMAIL_SENDER")
    parent_email = os.getenv("PARENT_ALERT_EMAIL")
    
    print("Configuration Check:")
    print(f"  SMTP_HOST: {smtp_host or '❌ NOT SET'}")
    print(f"  SMTP_PORT: {smtp_port or '❌ NOT SET'}")
    print(f"  SMTP_USERNAME: {smtp_user or '❌ NOT SET'}")
    print(f"  SMTP_PASSWORD: {'✅ SET' if smtp_pass else '❌ NOT SET'}")
    print(f"  EMAIL_SENDER: {email_sender or '❌ NOT SET'}")
    print(f"  PARENT_ALERT_EMAIL: {parent_email or '❌ NOT SET'}")
    print()
    
    if not all([smtp_host, smtp_user, smtp_pass, email_sender]):
        print("❌ SMTP not fully configured!")
        print()
        print("Add to .env:")
        print("  SMTP_HOST=smtp.gmail.com")
        print("  SMTP_PORT=587")
        print("  SMTP_USERNAME=your-gmail@gmail.com")
        print("  SMTP_PASSWORD=your_app_password")
        print("  EMAIL_SENDER=your-gmail@gmail.com")
        return False
    
    # Test email service
    try:
        from services.email_service import EmailService
        
        email_service = EmailService()
        
        print("Email Service Status:")
        print(f"  Configured: {email_service.is_configured()}")
        print(f"  Using SendGrid: {email_service.use_sendgrid}")
        print(f"  Using SMTP: {not email_service.use_sendgrid and email_service.is_configured()}")
        print()
        
        if not email_service.is_configured():
            print("❌ Email service not configured!")
            return False
        
        # Send test parent alert
        print("=" * 70)
        print("SENDING TEST PARENT ALERT")
        print("=" * 70)
        print()
        
        test_recipient = parent_email or smtp_user
        
        print(f"To: {test_recipient}")
        print(f"From: {email_sender}")
        print()
        
        # Create realistic parent alert
        subject = "🚨 ALERT: Your child attempted to access harmful content"
        
        body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #ff4444; border-radius: 10px; background-color: #fff5f5;">
        
        <h2 style="color: #ff4444; border-bottom: 2px solid #ff4444; padding-bottom: 10px;">
            🚨 PARENTAL ALERT - Anti-Lust Guardian
        </h2>
        
        <div style="background: #ffe6e6; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p style="margin: 0; font-size: 16px; font-weight: bold;">
                Your son or daughter tried to access harmful content.
            </p>
        </div>
        
        <h3 style="color: #333;">Incident Details:</h3>
        <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
            <tr style="background: #f9f9f9;">
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Child:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">test_child@example.com</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Content Type:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">NSFW Image</td>
            </tr>
            <tr style="background: #f9f9f9;">
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Confidence:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">98.5%</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Time:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">2024-12-03 23:50:00</td>
            </tr>
            <tr style="background: #f9f9f9;">
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Action Taken:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">✅ Content blocked</td>
            </tr>
        </table>
        
        <h3 style="color: #333;">What We Found Harmful:</h3>
        <ul style="background: #fff; padding: 15px 15px 15px 35px; border-left: 4px solid #ff4444; margin: 15px 0;">
            <li>Explicit adult content detected</li>
            <li>High confidence NSFW classification</li>
            <li>Blocked before display</li>
        </ul>
        
        <div style="background: #e6f7ff; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #0066cc;">
            <p style="margin: 0;"><strong>🛡️ Protection Status:</strong> Active</p>
            <p style="margin: 5px 0 0 0;">Your child's device is protected. This content was automatically blocked.</p>
        </div>
        
        <h3 style="color: #333;">Recommended Actions:</h3>
        <ol style="background: #fff; padding: 15px 15px 15px 35px;">
            <li>Talk to your child about online safety</li>
            <li>Review activity dashboard for patterns</li>
            <li>Consider adjusting protection settings if needed</li>
        </ol>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 12px;">
            <p>This is an automated alert from <strong>Anti-Lust Guardian</strong></p>
            <p>Protecting your family's digital wellbeing</p>
        </div>
        
    </div>
</body>
</html>
"""
        
        print("Sending test email...")
        
        # Use the notification service (the actual way emails are sent)
        from services.notification_service import NotificationService
        
        notifier = NotificationService()
        
        try:
            await notifier.send_critical_alert(
                device_id='test_device_123',
                parent_email=test_recipient,
                event_type='nsfw_detected',
                threat_level='HIGH',
                confidence=0.985,
                context={
                    'child_email': 'test_child@example.com',
                    'content_type': 'NSFW Image',
                    'timestamp': '2024-12-04 00:50:00',
                    'action': 'Content blocked'
                }
            )
            
            success = True
        except Exception as e:
            print(f"Error sending: {e}")
            success = False
        
        print()
        if success:
            print("✅ SUCCESS! Parent alert email sent!")
            print(f"✅ Check inbox: {test_recipient}")
            print()
            print("Email includes:")
            print("  • Child's email")
            print("  • What harmful content was found")
            print("  • Time of incident")
            print("  • Action taken (blocked)")
            print("  • Recommended actions for parent")
        else:
            print("❌ Failed to send email")
            print("Check:")
            print("  1. Gmail app password is correct")
            print("  2. 2-Step verification is enabled")
            print("  3. No spaces in app password")
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(test_gmail_smtp())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test cancelled")
        sys.exit(1)
