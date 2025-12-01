from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
import os
from datetime import datetime
import enum

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./guardian.db")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class AccountType(str, enum.Enum):
    SELF = "self"
    PARENT = "parent"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    account_type = Column(String, default=AccountType.SELF.value)
    pin_hash = Column(String, nullable=True)
    is_locked = Column(Boolean, default=False)
    emergency_mode = Column(Boolean, default=False)
    control_mode = Column(String(20), default='self')
    parent_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    parent_email = Column(String(255), nullable=True)
    allowed_hours_start = Column(Integer, default=0)
    allowed_hours_end = Column(Integer, default=24)
    blocked_apps = Column(Text, default='[]')
    allowed_apps = Column(Text, default='[]')
    vpn_detected_count = Column(Integer, default=0)
    uninstall_protected = Column(Boolean, default=True)
    pairing_code = Column(String(10), nullable=True, unique=True)
    parent_pin_hash = Column(String(255), nullable=True)
    pin_created_at = Column(DateTime, nullable=True)
    parent_phone_number = Column(String(20), nullable=True)
    remote_lock_until = Column(DateTime, nullable=True)
    remote_lock_reason = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    child_accounts = relationship('User', backref=backref('parent', remote_side=[id]), foreign_keys=[parent_id])
    policies = relationship("AppPolicy", back_populates="user")
    streak = relationship("FapStreak", uselist=False, back_populates="user")
    prevented_sites = relationship("PreventedSite", back_populates="user")

class GlobalBlocklist(Base):
    __tablename__ = "global_blocklist"
    
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, index=True)
    category = Column(String)
    added_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class AppPolicy(Base):
    __tablename__ = "app_policies"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    app_package = Column(String, index=True)
    app_name = Column(String)
    allow_chat = Column(Boolean, default=True)
    allow_feed = Column(Boolean, default=False)
    allow_calls = Column(Boolean, default=True)
    daily_limit_minutes = Column(Integer, default=30)
    is_whitelisted = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="policies")

class FapStreak(Base):
    __tablename__ = "fap_streaks"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    last_relapse = Column(DateTime, default=datetime.utcnow)
    current_streak_days = Column(Integer, default=0)
    best_streak_days = Column(Integer, default=0)
    total_relapses = Column(Integer, default=0)
    
    user = relationship("User", back_populates="streak")

class PreventedSite(Base):
    __tablename__ = "prevented_sites"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String)
    category = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    attempt_count = Column(Integer, default=1)
    notified_parent = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="prevented_sites")

class IllegalContentAttempt(Base):
    __tablename__ = "illegal_content_attempts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String)
    content_type = Column(String)
    ai_confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    parent_notified = Column(Boolean, default=False)
    session_terminated = Column(Boolean, default=False)

class MonthlyReport(Base):
    __tablename__ = "monthly_reports"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    month = Column(Integer)
    year = Column(Integer)
    total_threats_blocked = Column(Integer, default=0)
    total_time_saved_minutes = Column(Integer, default=0)
    pattern_analysis = Column(Text)
    pdf_generated = Column(Boolean, default=False)
    sent_to_parent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
