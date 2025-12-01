from sqlalchemy import Column, String, DateTime, Integer, Float, Text, ForeignKey, func, desc
from sqlalchemy.future import select
from datetime import datetime, timedelta
from database import Base, async_session, AppPolicy, User, FapStreak, PreventedSite
from typing import Dict, List, Optional
import random
import logging

logger = logging.getLogger(__name__)

class DopamineLimit(Base):
    __tablename__ = "dopamine_limits"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String, index=True)
    category = Column(String)
    daily_limit_minutes = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)

class DailyUsage(Base):
    __tablename__ = "daily_usage"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String, index=True)
    date = Column(DateTime, index=True)
    category = Column(String)
    minutes_used = Column(Float, default=0.0)

class DopamineService:
    def __init__(self):
        self.quotes = [
            "Your future needs you. Your past doesn't.",
            "Discipline is choosing between what you want now and what you want most.",
            "Don't let a screen control your destiny.",
            "The pain of discipline is far less than the pain of regret.",
            "Reclaim your mind. Reclaim your time.",
            "You are stronger than a dopamine hit.",
            "Greatness is built in the empty moments you refuse to fill with distractions.",
            "Focus is the new currency. Don't spend it on cheap thrills."
        ]
    
    async def check_feature_access(self, user_id: int, app_package: str, feature: str) -> Dict:
        """
        Granular check for Emergency Mode (e.g., Allow Chat, Block Feed).
        feature: 'chat', 'feed', 'call'
        """
        async with async_session() as session:
            user_result = await session.execute(select(User).where(User.id == user_id))
            user = user_result.scalar_one_or_none()
            
            if not user:
                return {"allowed": True} # Default allow if user not found (shouldn't happen)

            policy_result = await session.execute(
                select(AppPolicy).where(
                    AppPolicy.user_id == user_id,
                    AppPolicy.app_package == app_package
                )
            )
            policy = policy_result.scalar_one_or_none()
            
            if not policy:
                return {"allowed": True} # No specific policy
            
            if policy.is_whitelisted:
                return {"allowed": True, "reason": "whitelisted"}
            
            if user.emergency_mode:
                if feature == 'feed':
                    return {"allowed": False, "reason": "Emergency Mode: Feeds Blocked"}
                if feature == 'chat' or feature == 'call':
                    return {"allowed": True, "reason": "Emergency Mode: Communication Allowed"}
            
            if feature == 'feed' and not policy.allow_feed:
                return {"allowed": False, "reason": "Feed blocked by policy"}
            if feature == 'chat' and not policy.allow_chat:
                return {"allowed": False, "reason": "Chat blocked by policy"}
                
            return {"allowed": True}

    async def get_analytics(self, user_id: int) -> Dict:
        """
        Get Weekly/Monthly averages and comparisons.
        """
        async with async_session() as session:
            today = datetime.utcnow()
            last_month = today - timedelta(days=30)
            
            current_usage = await session.execute(
                select(func.sum(DailyUsage.minutes_used))
                .where(DailyUsage.date >= last_month)
            )
            total_minutes = current_usage.scalar() or 0
            
            prevented = await session.execute(
                select(PreventedSite)
                .where(PreventedSite.user_id == user_id)
                .order_by(desc(PreventedSite.timestamp))
                .limit(10)
            )
            prevented_list = [
                {"url": p.url, "date": p.timestamp.strftime("%Y-%m-%d"), "category": p.category}
                for p in prevented.scalars().all()
            ]
            
            streak_result = await session.execute(select(FapStreak).where(FapStreak.user_id == user_id))
            streak = streak_result.scalar_one_or_none()
            
            streak_data = {
                "current": streak.current_streak_days if streak else 0,
                "best": streak.best_streak_days if streak else 0,
                "last_relapse": streak.last_relapse.strftime("%Y-%m-%d") if streak else "Never"
            }
            
            return {
                "monthly_usage_hours": round(total_minutes / 60, 1),
                "prevented_sites": prevented_list,
                "streak": streak_data
            }

    async def reset_streak(self, user_id: int):
        async with async_session() as session:
            result = await session.execute(select(FapStreak).where(FapStreak.user_id == user_id))
            streak = result.scalar_one_or_none()
            
            if not streak:
                streak = FapStreak(user_id=user_id, current_streak_days=0, best_streak_days=0)
                session.add(streak)
            
            streak.current_streak_days = 0
            streak.last_relapse = datetime.utcnow()
            streak.total_relapses += 1
            
            await session.commit()
            return True

    async def set_limit(self, device_id: str, category: str, minutes: int):
        async with async_session() as session:
            result = await session.execute(
                select(DopamineLimit).where(
                    DopamineLimit.device_id == device_id,
                    DopamineLimit.category == category
                )
            )
            limit = result.scalar_one_or_none()
            
            if limit:
                limit.daily_limit_minutes = minutes
                limit.last_updated = datetime.utcnow()
            else:
                limit = DopamineLimit(
                    device_id=device_id,
                    category=category,
                    daily_limit_minutes=minutes
                )
                session.add(limit)
            
            await session.commit()
            logger.info(f"Limit set for {device_id}: {category} = {minutes}m")

    async def report_usage(self, device_id: str, category: str, minutes_delta: float) -> Dict:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        async with async_session() as session:
            result = await session.execute(
                select(DailyUsage).where(
                    DailyUsage.device_id == device_id,
                    DailyUsage.category == category,
                    DailyUsage.date == today
                )
            )
            usage = result.scalar_one_or_none()
            
            if usage:
                usage.minutes_used += minutes_delta
            else:
                usage = DailyUsage(
                    device_id=device_id,
                    date=today,
                    category=category,
                    minutes_used=minutes_delta
                )
                session.add(usage)
            
            await session.commit()
            current_usage = usage.minutes_used
            
            limit_result = await session.execute(
                select(DopamineLimit).where(
                    DopamineLimit.device_id == device_id,
                    DopamineLimit.category == category
                )
            )
            limit_obj = limit_result.scalar_one_or_none()
            
            if not limit_obj:
                return {"allowed": True, "message": "No limit set", "remaining": 9999}
            
            limit = limit_obj.daily_limit_minutes
            remaining = max(0, limit - current_usage)
            
            if current_usage >= limit:
                quote = random.choice(self.quotes)
                return {
                    "allowed": False,
                    "message": "Time Limit Exceeded",
                    "quote": quote,
                    "remaining": 0,
                    "usage": current_usage,
                    "limit": limit
                }
            
            return {
                "allowed": True,
                "message": "Access Granted",
                "remaining": remaining,
                "usage": current_usage,
                "limit": limit
            }

    async def get_status(self, device_id: str) -> Dict:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        async with async_session() as session:
            limits_result = await session.execute(
                select(DopamineLimit).where(DopamineLimit.device_id == device_id)
            )
            limits = limits_result.scalars().all()
            
            status = {}
            for l in limits:
                usage_result = await session.execute(
                    select(DailyUsage).where(
                        DailyUsage.device_id == device_id,
                        DailyUsage.category == l.category,
                        DailyUsage.date == today
                    )
                )
                usage = usage_result.scalar_one_or_none()
                used = usage.minutes_used if usage else 0
                
                status[l.category] = {
                    "limit": l.daily_limit_minutes,
                    "used": round(used, 1),
                    "remaining": max(0, l.daily_limit_minutes - used),
                    "is_blocked": used >= l.daily_limit_minutes
                }
            
            return status
