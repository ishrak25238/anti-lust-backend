import asyncio
from datetime import datetime, timedelta
from sqlalchemy import func
from database import MonthlyReport, User, PreventedSite, IllegalContentAttempt
from services.email_service import EmailService
from services.pattern_storage import PatternAnalyzer
import json

class MonthlyReportService:
    def __init__(self, db_session):
        self.db = db_session
        self.email_service = EmailService()
        self.pattern_analyzer = PatternAnalyzer(db_session)
    
    async def generate_monthly_report(self, user_id: int, month: int, year: int):
        user = await self.db.get(User, user_id)
        if not user:
            return None
        
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        threats_blocked = await self.db.execute(
            "SELECT COUNT(*) FROM prevented_sites WHERE user_id = :user_id AND timestamp >= :start AND timestamp < :end",
            {"user_id": user_id, "start": start_date, "end": end_date}
        )
        total_threats = threats_blocked.scalar()
        
        illegal_attempts = await self.db.execute(
            "SELECT COUNT(*) FROM illegal_content_attempts WHERE user_id = :user_id AND timestamp >= :start AND timestamp < :end",
            {"user_id": user_id, "start": start_date, "end": end_date}
        )
        total_illegal = illegal_attempts.scalar()
        
        patterns = await self.pattern_analyzer.analyze_user_patterns(user_id, days=30)
        
        time_saved = total_threats * 15
        
        report_data = {
            'user_id': user_id,
            'month': month,
            'year': year,
            'total_threats_blocked': total_threats,
            'total_illegal_attempts': total_illegal,
            'time_saved_minutes': time_saved,
            'peak_risk_hours': patterns.get('peak_hours', []),
            'most_blocked_categories': await self._get_top_categories(user_id, start_date, end_date),
            'streak_data': await self._get_streak_stats(user_id),
            'ai_insights': await self._generate_ai_insights(patterns, total_threats, total_illegal)
        }
        
        report = MonthlyReport(
            user_id=user_id,
            month=month,
            year=year,
            total_threats_blocked=total_threats,
            total_time_saved_minutes=time_saved,
            pattern_analysis=json.dumps(report_data),
            pdf_generated=False,
            sent_to_parent=False
        )
        self.db.add(report)
        await self.db.commit()
        
        return report
    
    async def _get_top_categories(self, user_id: int, start_date, end_date):
        results = await self.db.execute(
            "SELECT category, COUNT(*) as count FROM prevented_sites WHERE user_id = :user_id AND timestamp >= :start AND timestamp < :end GROUP BY category ORDER BY count DESC LIMIT 5",
            {"user_id": user_id, "start": start_date, "end": end_date}
        )
        return [{"category": row[0], "count": row[1]} for row in results.fetchall()]
    
    async def _get_streak_stats(self, user_id: int):
        streak = await self.db.execute(
            "SELECT current_streak_days, best_streak_days, total_relapses FROM fap_streaks WHERE user_id = :user_id",
            {"user_id": user_id}
        )
        row = streak.first()
        if row:
            return {
                'current_streak': row[0],
                'best_streak': row[1],
                'total_relapses': row[2]
            }
        return {'current_streak': 0, 'best_streak': 0, 'total_relapses': 0}
    
    async def _generate_ai_insights(self, patterns, total_threats, total_illegal):
        insights = []
        
        if total_threats > 100:
            insights.append("High threat activity detected. Consider implementing stricter time controls.")
        elif total_threats < 10:
            insights.append("Excellent self-control demonstrated this month!")
        
        if total_illegal > 0:
            insights.append(f"CRITICAL: {total_illegal} illegal content attempts detected. Immediate intervention recommended.")
        
        if patterns.get('peak_hours'):
            peak = patterns['peak_hours'][0] if patterns['peak_hours'] else 'evening'
            insights.append(f"Peak risk time: {peak}:00. Schedule positive activities during this hour.")
        
        return insights
    
    async def send_report_to_parent(self, report_id: int):
        report = await self.db.get(MonthlyReport, report_id)
        if not report:
            return False
        
        user = await self.db.get(User, report.user_id)
        if not user or not user.parent_email:
            return False
        
        report_data = json.loads(report.pattern_analysis)
        
        pdf_buffer = await self.email_service._generate_pdf_report(
            logs=[],
            device_id=str(user.id),
            ai_analysis=report_data
        )
        
        subject = f"Monthly Report - {report_data.get('month')}/{report_data.get('year')} - {user.email}"
        html_content = f"""
        <h2>Monthly Protection Report</h2>
        <p>Total Threats Blocked: {report.total_threats_blocked}</p>
        <p>Time Saved: {report.total_time_saved_minutes} minutes</p>
        <p>See attached PDF for detailed analysis.</p>
        """
        
        success = await self.email_service._send_via_sendgrid(
            subject, html_content, pdf_buffer, to_email=user.parent_email
        )
        
        if success:
            report.sent_to_parent = True
            await self.db.commit()
        
        return success
    
    async def auto_generate_monthly_reports(self):
        now = datetime.utcnow()
        last_month = now.month - 1 if now.month > 1 else 12
        year = now.year if now.month > 1 else now.year - 1
        
        users = await self.db.execute("SELECT id FROM users WHERE control_mode = 'parent'")
        
        for user in users.fetchall():
            existing = await self.db.execute(
                "SELECT id FROM monthly_reports WHERE user_id = :user_id AND month = :month AND year = :year",
                {"user_id": user[0], "month": last_month, "year": year}
            )
            
            if not existing.first():
                report = await self.generate_monthly_report(user[0], last_month, year)
                if report and report.user_id:
                    await self.send_report_to_parent(report.id)
        
        return True
