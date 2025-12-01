import os
from typing import List, Dict
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from datetime import datetime
import logging
import base64
from io import BytesIO
import asyncio

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.sendgrid_key = os.getenv("SENDGRID_API_KEY")
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.admin_email = os.getenv("ADMIN_EMAIL", "ishrakarafneo@gmail.com")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        if self.openai_key and OPENAI_AVAILABLE:
            openai.api_key = self.openai_key
        
        self.use_sendgrid = bool(self.sendgrid_key)
        self.max_retries = 3
    
    def is_configured(self) -> bool:
        return bool((self.sendgrid_key is not None) or \
               (self.smtp_host and self.smtp_username and self.smtp_password))
    
    async def send_research_report(self, logs: List[Dict], device_id: str):
        if not self.is_configured():
            raise Exception("Email not configured! Set SENDGRID_API_KEY or SMTP credentials")
        
        logger.info(f"Generating HARDCORE research report for device {device_id}")
        
        ai_analysis = await self._generate_gpt4_analysis(logs)
        
        pdf_buffer = await self._generate_pdf_report(logs, device_id, ai_analysis)
        
        html_content = self._generate_html_email(logs, device_id, ai_analysis)
        
        subject = f"🔴 CRITICAL: Deep Forensic Analysis - Device {device_id[:8]}"
        
        for attempt in range(self.max_retries):
            try:
                if self.use_sendgrid:
                    await self._send_via_sendgrid(subject, html_content, pdf_buffer)
                else:
                    await self._send_via_smtp(subject, html_content, pdf_buffer)
                
                logger.info(f"✅ REPORT SENT TO {self.admin_email}")
                return
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise Exception(f"Failed to send email after {self.max_retries} attempts: {e}")
    
    async def _generate_gpt4_analysis(self, logs: List[Dict]) -> Dict:
        if not self.openai_key or not OPENAI_AVAILABLE:
            logger.warning("OpenAI not configured or not available. Using heuristic analysis.")
            return self._heuristic_analysis(logs)
        
        try:
            log_summary = "\n".join([
                f"- {log.get('timestamp', 'N/A')}: {log.get('source', 'N/A')} → {log.get('reason', 'N/A')}"
                for log in logs[:50]
            ])
            
            prompt = f"""You are a forensic psychologist analyzing digital behavior patterns.

THREAT LOG DATA:
{log_summary}

Perform a DEEP analysis and provide:
1. PRIMARY BEHAVIORAL PATTERN (Compulsive/Opportunistic/Predatory/Addictive)
2. PSYCHOLOGICAL TRIGGERS identified
3. TEMPORAL PATTERNS (time of day, frequency)
4. ESCALATION VELOCITY (how fast behavior intensifies)
5. INTERVENTION STRATEGIES (specific, actionable)
6. RELAPSE RISK SCORE (0-100)

Be brutally honest. This is for clinical intervention."""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a forensic psychologist specializing in digital addiction."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return {
                "ai_analysis": response.choices[0].message.content,
                "model": "gpt-4",
                "confidence": 0.95
            }
        except Exception as e:
            logger.error(f"GPT-4 analysis failed: {e}")
            return self._heuristic_analysis(logs)
    
    def _heuristic_analysis(self, logs: List[Dict]) -> Dict:
        total = len(logs)
        adult_count = sum(1 for r in [log.get('reason', '') for log in logs] 
                         if 'adult' in r.lower() or 'porn' in r.lower())
        
        pattern = "PREDATORY / HIGH-RISK" if adult_count > total * 0.7 else "COMPULSIVE / BINGE" if total > 10 else "OPPORTUNISTIC"
        
        return {
            "ai_analysis": f"""PATTERN: {pattern}

STATISTICS:
- Total Blocks: {total}
- Adult Content: {adult_count} ({adult_count/total*100:.1f}% if total else 0)

INTERVENTION: Pattern indicates {pattern.lower()} behavior. Immediate lockdown recommended.""",
            "model": "heuristic",
            "confidence": 0.7
        }
    
    async def send_alert_email(self, to_email: str, subject: str, html_content: str):
        """Send a simple alert email without PDF attachment"""
        if not self.is_configured():
            logger.warning("Email not configured, skipping alert")
            return

        try:
            if self.use_sendgrid:
                message = Mail(from_email='alerts@antilustguardian.com', to_emails=to_email,
                             subject=subject, html_content=html_content)
                sg = SendGridAPIClient(self.sendgrid_key)
                sg.send(message)
            else:
                message = MIMEMultipart()
                message["From"], message["To"], message["Subject"] = self.smtp_username, to_email, subject
                message.attach(MIMEText(html_content, "html"))
                
                await aiosmtplib.send(message, hostname=self.smtp_host, port=self.smtp_port,
                                    username=self.smtp_username, password=self.smtp_password, start_tls=True)
        except Exception as e:
            logger.error(f"Failed to send alert email: {e}")

    async def _generate_pdf_report(self, logs: List[Dict], device_id: str, ai_analysis: Dict) -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18,
                                     textColor=colors.HexColor('#FF2A6D'), alignment=TA_CENTER, fontName='Helvetica-Bold')
        
        # Extract Solution/Intervention from AI Analysis
        analysis_text = ai_analysis['ai_analysis']
        
        story = [
            Paragraph("ANTI-LUST GUARDIAN - FORENSIC ANALYSIS", title_style),
            Spacer(1, 0.2*inch),
            Paragraph(f"Device: {device_id} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}", styles['Normal']),
            Spacer(1, 0.3*inch),
            Paragraph(f"Total Threats Blocked: {len(logs)}", styles['Heading2']),
            Spacer(1, 0.1*inch),
            Paragraph("AI PSYCHOLOGICAL PROFILE", styles['Heading3']),
            Paragraph(analysis_text.replace('\n', '<br/>'), styles['Normal']),
            Spacer(1, 0.2*inch),
            Paragraph("RECOMMENDED SOLUTIONS & INTERVENTION", styles['Heading3']),
            Paragraph("Based on the identified patterns, the following actions are recommended:", styles['Normal']),
            Spacer(1, 0.1*inch),
            Paragraph("1. Immediate Conversation: Discuss the specific triggers identified above.", styles['Normal']),
            Paragraph("2. Environment Change: Restrict device usage in private spaces (bedroom/bathroom).", styles['Normal']),
            Paragraph("3. Professional Help: Consider therapy if 'Addictive' pattern is high.", styles['Normal']),
            Paragraph("4. Dopamine Detox: Enable 'Emergency Mode' (Chat Only) for 7 days.", styles['Normal'])
        ]
        
        doc.build(story)
        buffer.seek(0)
        return buffer
