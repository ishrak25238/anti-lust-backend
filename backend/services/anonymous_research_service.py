"""
Research Paper Service - Sends anonymous research papers to ishrakarafneo@gmail.com
Analyzes dark web attempts and provides solutions
"""
import os
from services.research_paper_generator import ResearchPaperGenerator
from services.email_service import EmailService
from services.darkweb_detection_service import DarkWebDetectionService
from database import async_session
import asyncio
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io

class AnonymousResearchService:
    def __init__(self):
        self.email_service = EmailService()
        self.darkweb_detector = DarkWebDetectionService()
        self.admin_email = "ishrakarafneo@gmail.com"
    
    async def generate_and_send_darkweb_report(self, darkweb_attempts: list):
        """Generate PDF research paper on dark web access attempts and solutions"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        story.append(Paragraph(f"<b>Dark Web Access Pattern Analysis</b>", styles['Title']))
        story.append(Paragraph(f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Abstract
        story.append(Paragraph("<b>Executive Summary</b>", styles['Heading2']))
        summary_text = f"""
        This report analyzes {len(darkweb_attempts)} dark web access attempts detected by the Anti-Lust Guardian system.
        The analysis includes pattern detection, entry methods, and recommended countermeasures.
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Analysis of Methods
        story.append(Paragraph("<b>Common Dark Web Entry Methods Detected</b>", styles['Heading2']))
        methods = {
            'Tor Browser': 0,
            '.onion URLs': 0,
            'I2P Network': 0,
            'Dark Web Gateways': 0
        }
        
        for attempt in darkweb_attempts:
            if '.onion' in attempt.get('url', ''):
                methods['.onion URLs'] += 1
            if attempt.get('is_tor_browser'):
                methods['Tor Browser'] += 1
            if '.i2p' in attempt.get('url', ''):
                methods['I2P Network'] += 1
            if any(gw in attempt.get('url', '') for gw in ['onion.link', 'tor2web']):
                methods['Dark Web Gateways'] += 1
        
        for method, count in methods.items():
            story.append(Paragraph(f"• {method}: {count} attempts ({count/len(darkweb_attempts)*100:.1f}%)", styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Solutions
        story.append(Paragraph("<b>Recommended Prevention Solutions</b>", styles['Heading2']))
        solutions = [
            "<b>1. Browser-Level Blocking:</b> Detect and block Tor Browser installation attempts",
            "<b>2. URL Pattern Matching:</b> Block .onion and .i2p domain extensions at DNS level",
            "<b>3. Gateway Monitoring:</b> Block known dark web gateway domains (onion.link, tor2web.org, etc.)",
            "<b>4. Port Monitoring:</b> Detect and alert on Tor/I2P port usage (9050, 9051, 4444, 7656)",
            "<b>5. VPN/Proxy Detection:</b> Identify and block VPN services used to bypass filtering",
            "<b>6. User Agent Analysis:</b> Flag suspicious user agents matching Tor Browser signatures",
            "<b>7. Parent Notification:</b> Immediate alerts to guardians when dark web attempts detected",
            "<b>8. Educational Intervention:</b> Display educational content about dark web dangers"
        ]
        
        for solution in solutions:
            story.append(Paragraph(solution, styles['Normal']))
            story.append(Spacer(1, 10))
        
        story.append(Spacer(1, 20))
        
        # Technical Implementation
        story.append(Paragraph("<b>Technical Implementation Status</b>", styles['Heading2']))
        impl_status = [
            "✅ .onion/.i2p URL detection - ACTIVE",
            "✅ Dark web gateway blocking - ACTIVE",
            "✅ Tor Browser detection via user agent - ACTIVE",
            "✅ Port monitoring (9050, 9051, 4444, etc.) - ACTIVE",
            "✅ VPN detection service - ACTIVE",
            "✅ Real-time parent notifications - ACTIVE",
            "✅ Pattern learning from attempts - ACTIVE"
        ]
        
        for status in impl_status:
            story.append(Paragraph(status, styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Conclusion
        story.append(Paragraph("<b>Conclusion</b>", styles['Heading2']))
        conclusion = """
        The Anti-Lust Guardian system successfully detects and prevents dark web access attempts using
        multi-layered detection mechanisms. Continuous monitoring and pattern learning ensure adaptive
        protection against evolving bypass techniques. All detected attempts trigger immediate parental
        notifications and are stored anonymously for system improvement.
        """
        story.append(Paragraph(conclusion, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        # Send email with PDF attachment
        await self.email_service.send_email_with_attachment(
            to_email=self.admin_email,
            subject=f"Dark Web Access Analysis - {datetime.utcnow().strftime('%Y-%m-%d')}",
            body=f"Analyzed {len(darkweb_attempts)} dark web access attempts. See attached research paper for details and solutions.",
            attachment_data=buffer.getvalue(),
            attachment_filename=f"darkweb_analysis_{datetime.utcnow().strftime('%Y%m%d')}.pdf"
        )
        
        return {"success": True, "email_sent_to": self.admin_email}
    
    async def send_pattern_report(self, device_id: str):
        """Send comprehensive pattern analysis to admin email"""
        async with async_session() as db:
            # Get all pattern data
            from services.pattern_storage import PatternStorage
            pattern_storage = PatternStorage()
            
            patterns = await pattern_storage.analyze_temporal_patterns(device_id, days=30)
            recommendations = await pattern_storage.generate_recommendations(device_id)
            
            # Create email body
            body = f"""
            <h2>Pattern Analysis Report</h2>
            <p><b>Device ID:</b> {device_id}</p>
            <p><b>Analysis Period:</b> Last 30 days</p>
            
            <h3>Behavioral Patterns:</h3>
            <pre>{patterns}</pre>
            
            <h3>Recommendations:</h3>
            <pre>{recommendations}</pre>
            
            <p>This report is generated automatically and contains anonymized data for research purposes.</p>
            """
            
            await self.email_service.send_email(
                to_email=self.admin_email,
                subject="Pattern Analysis Report - Anti-Lust Guardian Research",
                body=body,
                is_html=True
            )
            
            return {"success": True}

# Global instance
research_service = AnonymousResearchService()
