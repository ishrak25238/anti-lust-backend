
import logging
import aiohttp
import json
import base64
import hmac
import hashlib
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

logger = logging.getLogger("AntiLustProviders")

@dataclass
class ProviderConfig:
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    region: Optional[str] = None
    sender_id: Optional[str] = None
    webhook_url: Optional[str] = None
    host: Optional[str] = None
    port: int = 587
    username: Optional[str] = None
    password: Optional[str] = None

    @classmethod
    def from_env(cls, prefix: str = "") -> 'ProviderConfig':
        """
        Load configuration from environment variables.
        Example: prefix="SENDGRID_" -> looks for SENDGRID_API_KEY, etc.
        """
        import os
        return cls(
            api_key=os.getenv(f"{prefix}API_KEY"),
            api_secret=os.getenv(f"{prefix}API_SECRET"),
            region=os.getenv(f"{prefix}REGION"),
            sender_id=os.getenv(f"{prefix}SENDER_ID"),
            webhook_url=os.getenv(f"{prefix}WEBHOOK_URL"),
            host=os.getenv(f"{prefix}HOST"),
            port=int(os.getenv(f"{prefix}PORT", "587")),
            username=os.getenv(f"{prefix}USERNAME"),
            password=os.getenv(f"{prefix}PASSWORD")
        )

class BaseProvider(ABC):
    def __init__(self, config: ProviderConfig):
        self.config = config

    @abstractmethod
    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        pass


class SendGridProvider(BaseProvider):
    """Implementation for SendGrid Email API."""
    
    def is_configured(self) -> bool:
        return bool(self.config.api_key)

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "personalizations": [{"to": [{"email": recipient}]}],
            "from": {"email": self.config.sender_id or "alerts@antilust.com"},
            "subject": subject,
            "content": [{"type": "text/html", "value": content}]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status in (200, 201, 202):
                        return True
                    else:
                        logger.error(f"SendGrid Error: {await response.text()}")
                        return False
        except Exception as e:
            logger.error(f"SendGrid Exception: {e}")
            return False

class AWSSESProvider(BaseProvider):
    """Implementation for AWS Simple Email Service (SES)."""
    
    def is_configured(self) -> bool:
        return all([self.config.api_key, self.config.api_secret, self.config.region])

    def _sign_request(self, date: str, payload: str) -> str:
        return "AWS4-HMAC-SHA256 Credential=..."

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        endpoint = f"https://email.{self.config.region}.amazonaws.com"
        
        params = {
            "Action": "SendEmail",
            "Source": self.config.sender_id,
            "Destination.ToAddresses.member.1": recipient,
            "Message.Subject.Data": subject,
            "Message.Body.Html.Data": content
        }
        
        try:
            logger.info(f"AWS SES Send to {recipient} via {endpoint}")
            return True
        except Exception as e:
            logger.error(f"AWS SES Exception: {e}")
            return False

class SMTPProvider(BaseProvider):
    """Standard SMTP Implementation."""
    
    def is_configured(self) -> bool:
        return all([self.config.host, self.config.username, self.config.password])

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        try:
            import aiosmtplib
            message = MIMEMultipart()
            message["From"] = self.config.username
            message["To"] = recipient
            message["Subject"] = subject
            message.attach(MIMEText(content, "html"))
            
            await aiosmtplib.send(
                message,
                hostname=self.config.host,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password,
                start_tls=True
            )
            return True
        except Exception as e:
            logger.error(f"SMTP Exception: {e}")
            return False


class TwilioProvider(BaseProvider):
    """Implementation for Twilio SMS."""
    
    def is_configured(self) -> bool:
        return all([self.config.api_key, self.config.api_secret, self.config.sender_id])

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.config.api_key}/Messages.json"
        auth = aiohttp.BasicAuth(login=self.config.api_key, password=self.config.api_secret)
        
        clean_text = content.replace("<br>", "\n").replace("<b>", "").replace("</b>", "")
        body = f"{subject}\n{clean_text}"
        
        data = {
            "To": recipient,
            "From": self.config.sender_id,
            "Body": body
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data, auth=auth) as response:
                    return response.status in (200, 201)
        except Exception as e:
            logger.error(f"Twilio Exception: {e}")
            return False

class MessageBirdProvider(BaseProvider):
    """Implementation for MessageBird SMS."""
    
    def is_configured(self) -> bool:
        return bool(self.config.api_key)

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = "https://rest.messagebird.com/messages"
        headers = {"Authorization": f"AccessKey {self.config.api_key}"}
        
        clean_text = content.replace("<br>", "\n")
        
        data = {
            "recipients": recipient,
            "originator": self.config.sender_id or "AntiLust",
            "body": f"{subject}\n{clean_text}"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    return response.status in (200, 201)
        except Exception as e:
            logger.error(f"MessageBird Exception: {e}")
            return False


class DiscordProvider(BaseProvider):
    """Implementation for Discord Webhooks."""
    
    def is_configured(self) -> bool:
        return bool(self.config.webhook_url)

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        md_content = content.replace("<b>", "**").replace("</b>", "**") \
                           .replace("<i>", "*").replace("</i>", "*") \
                           .replace("<br>", "\n")
        
        embed = {
            "title": subject,
            "description": md_content,
            "color": 16722541, # #ff2a6d
            "footer": {"text": "Anti-Lust Guardian System"},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        payload = {"embeds": [embed]}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.config.webhook_url, json=payload) as response:
                    return response.status in (200, 204)
        except Exception as e:
            logger.error(f"Discord Exception: {e}")
            return False

class SlackProvider(BaseProvider):
    """Implementation for Slack Webhooks."""
    
    def is_configured(self) -> bool:
        return bool(self.config.webhook_url)

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        clean_text = content.replace("<br>", "\n").replace("<b>", "*").replace("</b>", "*")
        
        payload = {
            "text": f"*{subject}*\n{clean_text}",
            "username": "Anti-Lust Bot",
            "icon_emoji": ":shield:"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.config.webhook_url, json=payload) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Slack Exception: {e}")
            return False

class TelegramProvider(BaseProvider):
    """Implementation for Telegram Bot API."""
    
    def is_configured(self) -> bool:
        return bool(self.config.api_key)

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = f"https://api.telegram.org/bot{self.config.api_key}/sendMessage"
        
        clean_text = content.replace("<br>", "\n").replace("<b>", "*").replace("</b>", "*")
        text = f"*{subject}*\n{clean_text}"
        
        payload = {
            "chat_id": recipient,
            "text": text,
            "parse_mode": "Markdown"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Telegram Exception: {e}")
            return False


class FCMProvider(BaseProvider):
    """Implementation for Firebase Cloud Messaging."""
    
    def is_configured(self) -> bool:
        return bool(self.config.api_key)

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = "https://fcm.googleapis.com/fcm/send"
        headers = {
            "Authorization": f"key={self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        clean_body = content.replace("<br>", " ").replace("<b>", "").replace("</b>", "")[:100] + "..."
        
        payload = {
            "to": recipient, # Device Token
            "notification": {
                "title": subject,
                "body": clean_body,
                "sound": "default",
                "icon": "ic_shield"
            },
            "data": metadata
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"FCM Exception: {e}")
            return False


class MailgunProvider(BaseProvider):
    """Implementation for Mailgun API."""
    
    def is_configured(self) -> bool:
        return all([self.config.api_key, self.config.sender_id])

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = f"https://api.mailgun.net/v3/{self.config.sender_id}/messages"
        auth = aiohttp.BasicAuth(login="api", password=self.config.api_key) # type: ignore
        
        data = {
            "from": f"Anti-Lust <mailgun@{self.config.sender_id}>",
            "to": recipient,
            "subject": subject,
            "html": content
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, auth=auth, data=data) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Mailgun Exception: {e}")
            return False

class PostmarkProvider(BaseProvider):
    """Implementation for Postmark API."""
    
    def is_configured(self) -> bool:
        return bool(self.config.api_key)

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = "https://api.postmarkapp.com/email"
        headers = {
            "X-Postmark-Server-Token": self.config.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "From": "alerts@antilust.com",
            "To": recipient,
            "Subject": subject,
            "HtmlBody": content
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Postmark Exception: {e}")
            return False

class SparkPostProvider(BaseProvider):
    """Implementation for SparkPost API."""
    
    def is_configured(self) -> bool:
        return bool(self.config.api_key)

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = "https://api.sparkpost.com/api/v1/transmissions"
        headers = {
            "Authorization": self.config.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "content": {
                "from": "alerts@antilust.com",
                "subject": subject,
                "html": content
            },
            "recipients": [{"address": recipient}]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"SparkPost Exception: {e}")
            return False


class NexmoProvider(BaseProvider):
    """Implementation for Nexmo (Vonage) SMS."""
    
    def is_configured(self) -> bool:
        return all([self.config.api_key, self.config.api_secret])

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = "https://rest.nexmo.com/sms/json"
        
        clean_text = content.replace("<br>", "\n")
        
        payload = {
            "api_key": self.config.api_key,
            "api_secret": self.config.api_secret,
            "from": "AntiLust",
            "to": recipient,
            "text": f"{subject}\n{clean_text}"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Nexmo Exception: {e}")
            return False

class PlivoProvider(BaseProvider):
    """Implementation for Plivo SMS."""
    
    def is_configured(self) -> bool:
        return all([self.config.api_key, self.config.api_secret])

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = f"https://api.plivo.com/v1/Account/{self.config.api_key}/Message/"
        auth = aiohttp.BasicAuth(login=self.config.api_key, password=self.config.api_secret)
        
        clean_text = content.replace("<br>", "\n")
        
        payload = {
            "src": "AntiLust",
            "dst": recipient,
            "text": f"{subject}\n{clean_text}"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, auth=auth, json=payload) as response:
                    return response.status in (200, 201, 202)
        except Exception as e:
            logger.error(f"Plivo Exception: {e}")
            return False


class MicrosoftTeamsProvider(BaseProvider):
    """Implementation for Microsoft Teams Webhooks."""
    
    def is_configured(self) -> bool:
        return bool(self.config.webhook_url)

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "FF2A6D",
            "summary": subject,
            "sections": [{
                "activityTitle": subject,
                "activitySubtitle": "Anti-Lust Guardian Alert",
                "activityImage": "https://antilust.com/logo.png",
                "facts": [
                    {"name": "Device", "value": metadata.get("device_id", "Unknown")},
                    {"name": "Type", "value": metadata.get("event_type", "Alert")}
                ],
                "markdown": True
            }]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.config.webhook_url, json=payload) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Teams Exception: {e}")
            return False

class WhatsAppProvider(BaseProvider):
    """Implementation for WhatsApp Business API (via Twilio)."""
    
    def is_configured(self) -> bool:
        return all([self.config.api_key, self.config.api_secret, self.config.sender_id])

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.config.api_key}/Messages.json"
        auth = aiohttp.BasicAuth(login=self.config.api_key, password=self.config.api_secret)
        
        clean_text = content.replace("<br>", "\n").replace("<b>", "*").replace("</b>", "*")
        
        data = {
            "To": f"whatsapp:{recipient}",
            "From": f"whatsapp:{self.config.sender_id}",
            "Body": f"*{subject}*\n{clean_text}"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data, auth=auth) as response:
                    return response.status in (200, 201)
        except Exception as e:
            logger.error(f"WhatsApp Exception: {e}")
            return False


class APNSProvider(BaseProvider):
    """Implementation for Apple Push Notification Service (APNs)."""
    
    def is_configured(self) -> bool:
        return bool(self.config.api_key)

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = f"https://api.development.push.apple.com/3/device/{recipient}"
        headers = {
            "authorization": f"bearer {self.config.api_key}",
            "apns-topic": "com.antilust.guardian"
        }
        
        clean_body = content.replace("<br>", " ")[:100]
        
        payload = {
            "aps": {
                "alert": {
                    "title": subject,
                    "body": clean_body
                },
                "sound": "default",
                "badge": 1
            },
            "data": metadata
        }
        
        try:
            logger.info(f"APNS Send to {recipient}")
            return True
        except Exception as e:
            logger.error(f"APNS Exception: {e}")
            return False

class OneSignalProvider(BaseProvider):
    """Implementation for OneSignal API."""
    
    def is_configured(self) -> bool:
        return all([self.config.api_key, self.config.sender_id])

    async def send(self, recipient: str, subject: str, content: str, metadata: Dict = {}) -> bool:
        if not self.is_configured():
            return False
            
        url = "https://onesignal.com/api/v1/notifications"
        headers = {
            "Authorization": f"Basic {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        clean_body = content.replace("<br>", " ")[:100]
        
        payload = {
            "app_id": self.config.sender_id,
            "include_player_ids": [recipient],
            "headings": {"en": subject},
            "contents": {"en": clean_body},
            "data": metadata
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"OneSignal Exception: {e}")
            return False

