"""
Database migration: Add security and pattern analysis tables
Run with: python migrations/add_security_tables.py
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Column, String, DateTime, Integer, Float, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./guardian.db")
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()


class ParentChildLink(Base):
    __tablename__ = "parent_child_links"
    id = Column(Integer, primary_key=True)
    parent_email = Column(String, index=True)
    child_code = Column(String, unique=True)
    child_name = Column(String)
    device_id = Column(String, unique=True)
    created_at = Column(DateTime)

class ThreatLogModel(Base):
    __tablename__ = "threat_logs"
    id = Column(Integer, primary_key=True)
    device_id = Column(String, ForeignKey("parent_child_links.device_id"))
    source = Column(String)
    reason = Column(String)
    context = Column(Text)
    timestamp = Column(DateTime)

class PatternEvent(Base):
    __tablename__ = "pattern_events"
    id = Column(Integer, primary_key=True)
    device_id = Column(String, index=True)
    event_type = Column(String)
    confidence = Column(Float)
    threat_level = Column(Integer)
    threat_score = Column(Float)
    context = Column(JSON)
    timestamp = Column(DateTime, index=True)
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
    last_updated = Column(DateTime)

class InterventionRecommendation(Base):
    __tablename__ = "intervention_recommendations"
    id = Column(Integer, primary_key=True)
    device_id = Column(String, index=True)
    recommendation = Column(Text)
    priority = Column(Integer)
    category = Column(String)
    created_at = Column(DateTime)
    acknowledged = Column(Integer, default=0)
    effective = Column(Integer, default=0)

class FalsePositiveReport(Base):
    __tablename__ = "false_positive_reports"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("pattern_events.id"))
    device_id = Column(String)
    reason = Column(Text)
    reported_at = Column(DateTime)
    reviewed = Column(Integer, default=0)

class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True)
    key_hash = Column(String, unique=True, index=True)
    name = Column(String)
    user_id = Column(String, nullable=True)
    created_at = Column(DateTime)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Integer, default=1)
    last_used = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0)

class UserSession(Base):
    __tablename__ = "user_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    token_hash = Column(String, unique=True)
    created_at = Column(DateTime)
    expires_at = Column(DateTime)
    ip_address = Column(String)
    user_agent = Column(String, nullable=True)
    is_valid = Column(Integer, default=1)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    event_type = Column(String, index=True)
    user_id = Column(String, nullable=True, index=True)
    device_id = Column(String, nullable=True)
    ip_address = Column(String)
    user_agent = Column(String, nullable=True)
    resource = Column(String, nullable=True)
    action = Column(String, nullable=True)
    result = Column(String)
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, index=True)

async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("\n✅ All security and pattern analysis tables created successfully!")
    print("\nCreated tables:")
    print("  - parent_child_links (existing)")
    print("  - threat_logs (existing)")
    print("  - api_keys (API key management)")
    print("  - user_sessions (JWT session tracking)")
    print("  - audit_logs (Security event logging)")
    print("  - pattern_events (ML pattern storage)")
    print("  - daily_pattern_summaries (Aggregated statistics)")
    print("  - behavioral_profiles (Long-term behavioral trends)")
    print("  - intervention_recommendations (Actionable suggestions)")
    print("  - false_positive_reports (ML feedback loop)")
    print("\n✅ Database migration complete!")

if __name__ == "__main__":
    asyncio.run(create_tables())

