from sqlalchemy import Column, String, DateTime, Integer, Float, Text, ForeignKey, JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, or_
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from database import Base, async_session
import json
import logging

logger = logging.getLogger(__name__)

class PatternEvent(Base):
    __tablename__ = "pattern_events"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String, index=True)
    event_type = Column(String)
    confidence = Column(Float)
    threat_level = Column(Integer)
    threat_score = Column(Float)
    context = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    is_false_positive = Column(Integer, default=0)

class DailyPatternSummary(Base):
    __tablename__ = "daily_pattern_summaries"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String, index=True)
    date = Column(DateTime, index=True)
    total_events = Column(Integer)
    nsfw_count = Column(Integer)
    text_count = Column(Integer)
    url_count = Column(Integer)
    avg_threat_score = Column(Float)
    peak_hour = Column(Integer)
    escalation_detected = Column(Integer, default=0)
    relapse_risk_score = Column(Float)

class BehavioralProfile(Base):
    __tablename__ = "behavioral_profiles"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String, unique=True, index=True)
    first_event = Column(DateTime)
    last_event = Column(DateTime)
    total_events = Column(Integer)
    avg_daily_events = Column(Float)
    peak_hours = Column(JSON)
    peak_days = Column(JSON)
    trend = Column(String)
    habit_formation_score = Column(Float)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)

class InterventionRecommendation(Base):
    __tablename__ = "intervention_recommendations"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String, index=True)
    recommendation = Column(Text)
    priority = Column(Integer)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    acknowledged = Column(Integer, default=0)
    effective = Column(Integer, default=0)

class FalsePositiveReport(Base):
    __tablename__ = "false_positive_reports"
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("pattern_events.id"))
    device_id = Column(String)
    reason = Column(Text)
    reported_at = Column(DateTime, default=datetime.utcnow)
    reviewed = Column(Integer, default=0)

class PatternStorage:
    async def store_event(self, device_id: str, event_type: str, 
                         confidence: float, threat_level: int, 
                         threat_score: float, context: Dict) -> int:
        async with async_session() as session:
            event = PatternEvent(
                device_id=device_id,
                event_type=event_type,
                confidence=confidence,
                threat_level=threat_level,
                threat_score=threat_score,
                context=context
            )
            session.add(event)
            await session.commit()
            await session.refresh(event)
            
            await self._update_behavioral_profile(device_id)
            
            return event.id
    
    async def get_events(self, device_id: str, hours: int = 24) -> List[Dict]:
        async with async_session() as session:
            cutoff = datetime.utcnow() - timedelta(hours=hours)
            result = await session.execute(
                select(PatternEvent).where(
                    and_(
                        PatternEvent.device_id == device_id,
                        PatternEvent.timestamp >= cutoff
                    )
                ).order_by(PatternEvent.timestamp.desc())
            )
            events = result.scalars().all()
            
            return [{
                'id': e.id,
                'event_type': e.event_type,
                'confidence': e.confidence,
                'threat_level': e.threat_level,
                'threat_score': e.threat_score,
                'context': e.context,
                'timestamp': e.timestamp.isoformat(),
                'is_false_positive': e.is_false_positive
            } for e in events]
    
    async def analyze_temporal_patterns(self, device_id: str, days: int = 7) -> Dict[str, Any]:
        async with async_session() as session:
            cutoff = datetime.utcnow() - timedelta(days=days)
            result = await session.execute(
                select(PatternEvent).where(
                    and_(
                        PatternEvent.device_id == device_id,
                        PatternEvent.timestamp >= cutoff
                    )
                )
            )
            events = result.scalars().all()
            
            if len(events) < 5:
                return {'status': 'insufficient_data', 'events_count': len(events)}
            
            total = len(events)
            per_day = total / days
            
            hours = [e.timestamp.hour for e in events]
            hour_counts = {}
            for h in hours:
                hour_counts[h] = hour_counts.get(h, 0) + 1
            peak_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            
            days_of_week = [e.timestamp.weekday() for e in events]
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
            mid = len(events) // 2
            first_half = events[:mid]
            second_half = events[mid:]
            
            first_avg = sum(e.threat_score for e in first_half) / len(first_half)
            second_avg = sum(e.threat_score for e in second_half) / len(second_half)
            delta = second_avg - first_avg
            escalating = delta > 0.2
            
            day_ago = datetime.utcnow() - timedelta(hours=24)
            recent = [e for e in events if e.timestamp >= day_ago]
            
            if len(recent) > 10:
                risk_score, risk_level = 0.9, "CRITICAL"
            elif len(recent) > 5:
                risk_score, risk_level = 0.7, "HIGH"
            elif len(recent) > 2:
                risk_score, risk_level = 0.4, "MODERATE"
            else:
                risk_score, risk_level = 0.2, "LOW"
            
            return {
                'frequency': {
                    'total_events': total,
                    'per_day': round(per_day, 2),
                    'category': 'CRITICAL' if per_day > 5 else 'HIGH' if per_day > 2 else 'MODERATE' if per_day > 0.5 else 'LOW'
                },
                'temporal': {
                    'peak_hours': [h for h, _ in peak_hours],
                    'hour_distribution': hour_counts
                },
                'escalation': {
                    'detected': escalating,
                    'delta': round(delta, 3),
                    'trend': 'ESCALATING' if escalating else 'STABLE'
                },
                'relapse_risk': {
                    'score': risk_score,
                    'level': risk_level,
                    'events_24h': len(recent)
                },
                'status': 'analyzed'
            }
    
    async def generate_recommendations(self, device_id: str) -> List[Dict]:
        patterns = await self.analyze_temporal_patterns(device_id)
        
        if patterns.get('status') != 'analyzed':
            return []
        
        recommendations = []
        
        if patterns['frequency']['category'] == 'CRITICAL':
            recommendations.append({
                'priority': 10,
                'category': 'IMMEDIATE',
                'recommendation': 'Enable Guardian Lock immediately - Critical usage frequency detected'
            })
        
        if patterns['relapse_risk']['level'] in ['HIGH', 'CRITICAL']:
            recommendations.append({
                'priority': 9,
                'category': 'IMMEDIATE',
                'recommendation': f"High relapse risk detected ({patterns['relapse_risk']['events_24h']} events in 24h) - Schedule intervention call"
            })
        
        if patterns['escalation']['detected']:
            recommendations.append({
                'priority': 8,
                'category': 'WARNING',
                'recommendation': f"Behavioral escalation detected (trend: {patterns['escalation']['trend']}) - Increase monitoring"
            })
        
        if patterns['temporal']['peak_hours']:
            peak = patterns['temporal']['peak_hours'][0]
            recommendations.append({
                'priority': 6,
                'category': 'SUGGESTION',
                'recommendation': f"Schedule positive activities at peak risk hour: {peak}:00"
            })
        
        async with async_session() as session:
            for rec in recommendations:
                intervention = InterventionRecommendation(
                    device_id=device_id,
                    recommendation=rec['recommendation'],
                    priority=rec['priority'],
                    category=rec['category']
                )
                session.add(intervention)
            await session.commit()
        
        return recommendations
    
    async def _update_behavioral_profile(self, device_id: str):
        async with async_session() as session:
            result = await session.execute(
                select(PatternEvent).where(PatternEvent.device_id == device_id)
            )
            events = result.scalars().all()
            
            if not events:
                return
            
            first_event = min(e.timestamp for e in events)
            last_event = max(e.timestamp for e in events)
            total_events = len(events)
            days = (last_event - first_event).days + 1
            avg_daily = total_events / days if days > 0 else 0
            
            hours = [e.timestamp.hour for e in events]
            hour_counts = {}
            for h in hours:
                hour_counts[h] = hour_counts.get(h, 0) + 1
            peak_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            peak_hour_list = [h for h, _ in peak_hours]
            
            now = datetime.utcnow()
            week_ago = now - timedelta(days=7)
            two_weeks_ago = now - timedelta(days=14)
            
            last_week = [e for e in events if week_ago <= e.timestamp <= now]
            prev_week = [e for e in events if two_weeks_ago <= e.timestamp < week_ago]
            
            if len(prev_week) > 0 and len(last_week) > 0:
                last_avg = len(last_week) / 7
                prev_avg = len(prev_week) / 7
                if last_avg < prev_avg * 0.7:
                    trend = 'IMPROVING'
                elif last_avg > prev_avg * 1.3:
                    trend = 'WORSENING'
                else:
                    trend = 'STABLE'
            else:
                trend = 'STABLE'
            
            result = await session.execute(
                select(BehavioralProfile).where(BehavioralProfile.device_id == device_id)
            )
            profile = result.scalar_one_or_none()
            
            if profile:
                profile.last_event = last_event
                profile.total_events = total_events
                profile.avg_daily_events = avg_daily
                profile.peak_hours = peak_hour_list
                profile.trend = trend
                profile.last_updated = datetime.utcnow()
            else:
                profile = BehavioralProfile(
                    device_id=device_id,
                    first_event=first_event,
                    last_event=last_event,
                    total_events=total_events,
                    avg_daily_events=avg_daily,
                    peak_hours=peak_hour_list,
                    peak_days=[],
                    trend=trend,
                    habit_formation_score=0.0
                )
                session.add(profile)
            
            await session.commit()
    
    async def report_false_positive(self, event_id: int, device_id: str, reason: str) -> int:
        async with async_session() as session:
            result = await session.execute(
                select(PatternEvent).where(PatternEvent.id == event_id)
            )
            event = result.scalar_one_or_none()
            
            if event:
                event.is_false_positive = 1
            
            report = FalsePositiveReport(
                event_id=event_id,
                device_id=device_id,
                reason=reason
            )
            session.add(report)
            await session.commit()
            await session.refresh(report)
            
            logger.info(f"False positive reported: event_id={event_id}, device={device_id}")
            return report.id
    
    async def get_behavioral_profile(self, device_id: str) -> Optional[Dict]:
        async with async_session() as session:
            result = await session.execute(
                select(BehavioralProfile).where(BehavioralProfile.device_id == device_id)
            )
            profile = result.scalar_one_or_none()
            
            if not profile:
                return None
            
            return {
                'device_id': profile.device_id,
                'first_event': profile.first_event.isoformat(),
                'last_event': profile.last_event.isoformat(),
                'total_events': profile.total_events,
                'avg_daily_events': profile.avg_daily_events,
                'peak_hours': profile.peak_hours,
                'trend': profile.trend,
                'habit_formation_score': profile.habit_formation_score
            }


class PatternAnalyzer:
    """
    Analyzer for user behavioral patterns.
    Wraps PatternLearningEngine for single-user analysis.
    """
    def __init__(self, db_session):
        self.db = db_session
        from services.pattern_learning_engine import PatternLearningEngine
        self.engine = PatternLearningEngine()

    async def analyze_user_patterns(self, user_id: int, days: int = 30) -> Dict:
        """
        Analyzes patterns for a single user.
        Returns dict with 'peak_hours', etc.
        """
        try:
            pattern = await self.engine._extract_user_pattern(user_id, self.db)
            if pattern:
                return pattern
            return {'peak_hours': []}
        except Exception as e:
            logger.error(f"Pattern analysis failed for user {user_id}: {e}")
            return {'peak_hours': []}
