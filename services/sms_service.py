import os
import asyncio
from typing import Optional

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    Client = None

class SMSNotificationService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if TWILIO_AVAILABLE and self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
    
    async def send_sms(self, to_number: str, message: str) -> bool:
        if not self.enabled:
            return False
        
        try:
            cleaned_number = to_number.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
            if not cleaned_number.startswith('+'):
                cleaned_number = '+' + cleaned_number
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.client.messages.create(
                    body=message,
                    from_=self.from_number,
                    to=cleaned_number
                )
            )
            return True
        except Exception as e:
            print(f"SMS send error: {e}")
            return False
    
    async def send_pin_alert(self, phone_number: str, event_type: str, details: dict) -> bool:
        messages = {
            'remote_lock': f"🔒 PARENT ALERT: Child device locked remotely for {details.get('duration', 0)} minutes. Reason: {details.get('reason', 'None')}",
            'uninstall_attempt_allowed': f"✅ PARENT ALERT: App uninstall allowed with correct PIN. Child: {details.get('child_email', 'Unknown')}",
            'uninstall_attempt_denied': f"❌ PARENT ALERT: App uninstall attempt DENIED - Invalid PIN! Child: {details.get('child_email', 'Unknown')}. Time: {details.get('timestamp', 'Now')}",
            'vpn_detected': f"⚠️ PARENT ALERT: VPN detected on child device! Detection count: {details.get('detection_count', 0)}. Child: {details.get('child_email', 'Unknown')}",
            'illegal_content': f"🚨 CRITICAL ALERT: Illegal content blocked! Child: {details.get('child_email', 'Unknown')}. Confidence: {details.get('confidence', '0')}%"
        }
        
        message = messages.get(event_type, f"PARENT ALERT: {event_type}")
        return await self.send_sms(phone_number, message)
    
    async def send_pin_creation_confirmation(self, phone_number: str) -> bool:
        message = "✅ Parent PIN successfully created for Anti-Lust Guardian. Your child's device is now protected."
        return await self.send_sms(phone_number, message)
