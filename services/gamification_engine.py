"""
Gamification System - Achievement, rewards, and motivation engine
Transforms recovery journey into an engaging, goal-oriented experience.
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class AchievementTier(Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


class CategoryType(Enum):
    STREAK = "streak"
    RESISTANCE = "resistance"
    GROWTH = "growth"
    SOCIAL = "social"
    MASTERY = "mastery"


@dataclass
class Achievement:
    achievement_id: str
    title: str
    description: str
    tier: AchievementTier
    category: CategoryType
    points: int
    icon: str
    unlock_criteria: Dict
    secret: bool = False
    repeatable: bool = False


@dataclass
class UserProgress:
    user_id: str
    total_points: int
    level: int
    achievements_unlocked: List[str]
    current_streak: int
    longest_streak: int
    total_threats_blocked: int
    join_date: datetime


class GamificationEngine:
    """Comprehensive gamification system for user engagement and motivation."""
    
    def __init__(self):
        self.achievements = self._initialize_achievements()
        self.level_thresholds = self._calculate_level_thresholds()
        
    def _initialize_achievements(self) -> List[Achievement]:
        """Initialize all available achievements."""
        
        achievements = []
        
        achievements.extend([
            Achievement(
                achievement_id="first_day",
                title="Day One Warrior",
                description="Complete your first day of protection",
                tier=AchievementTier.BRONZE,
                category=CategoryType.STREAK,
                points=10,
                icon="🏁",
                unlock_criteria={"streak_days": 1}
            ),
            Achievement(
                achievement_id="week_one",
                title="Seven Days Strong",
                description="Maintain a 7-day clean streak",
                tier=AchievementTier.SILVER,
                category=CategoryType.STREAK,
                points=50,
                icon="📅",
                unlock_criteria={"streak_days": 7}
            ),
            Achievement(
                achievement_id="month_warrior",
                title="Month Milestone",
                description="Achieve a 30-day clean streak",
                tier=AchievementTier.GOLD,
                category=CategoryType.STREAK,
                points=200,
                icon="🏆",
                unlock_criteria={"streak_days": 30}
            ),
            Achievement(
                achievement_id="quarter_champion",
                title="90-Day Champion",
                description="Conquer 90 consecutive days",
                tier=AchievementTier.PLATINUM,
                category=CategoryType.STREAK,
                points=500,
                icon="👑",
                unlock_criteria={"streak_days": 90}
            ),
            Achievement(
                achievement_id="half_year_legend",
                title="Six-Month Legend",
                description="Unbreakable: 180 days of excellence",
                tier=AchievementTier.DIAMOND,
                category=CategoryType.STREAK,
                points=1000,
                icon="💎",
                unlock_criteria={"streak_days": 180}
            ),
        ])
        
        achievements.extend([
            Achievement(
                achievement_id="first_block",
                title="Guardian Activated",
                description="Successfully block your first threat",
                tier=AchievementTier.BRONZE,
                category=CategoryType.RESISTANCE,
                points=5,
                icon="🛡️",
                unlock_criteria={"threats_blocked": 1}
            ),
            Achievement(
                achievement_id="ten_blocks",
                title="Threat Terminator",
                description="Block 10 threats",
                tier=AchievementTier.BRONZE,
                category=CategoryType.RESISTANCE,
                points=25,
                icon="⚔️",
                unlock_criteria={"threats_blocked": 10}
            ),
            Achievement(
                achievement_id="hundred_blocks",
                title="Fortress Commander",
                description="Block 100 threats - you're unstoppable",
                tier=AchievementTier.GOLD,
                category=CategoryType.RESISTANCE,
                points=150,
                icon="🏰",
                unlock_criteria={"threats_blocked": 100}
            ),
            Achievement(
                achievement_id="thousand_blocks",
                title="Digital Sentinel",
                description="1000 threats neutralized - legendary status",
                tier=AchievementTier.DIAMOND,
                category=CategoryType.RESISTANCE,
                points=750,
                icon="🛡️✨",
                unlock_criteria={"threats_blocked": 1000}
            ),
        ])
        
        achievements.extend([
            Achievement(
                achievement_id="early_riser",
                title="Early Bird Wisdom",
                description="Complete 7 days with no threats before 10 AM",
                tier=AchievementTier.SILVER,
                category=CategoryType.GROWTH,
                points=75,
                icon="🌅",
                unlock_criteria={"morning_clean_days": 7},
                secret=True
            ),
            Achievement(
                achievement_id="night_owl_reformed",
                title="Night Owl Reformed",
                description="No late-night (10 PM - 2 AM) threats for 14 days",
                tier=AchievementTier.GOLD,
                category=CategoryType.GROWTH,
                points=150,
                icon="🦉",
                unlock_criteria={"night_clean_days": 14},
                secret=True
            ),
            Achievement(
                achievement_id="perfect_week",
                title="Flawless Victory",
                description="Complete a week with zero threats detected",
                tier=AchievementTier.PLATINUM,
                category=CategoryType.GROWTH,
                points=300,
                icon="⭐",
                unlock_criteria={"perfect_days": 7}
            ),
        ])
        
        achievements.extend([
            Achievement(
                achievement_id="helper",
                title="Supporting Guardian",
                description="Help another user through referral or mentorship",
                tier=AchievementTier.SILVER,
                category=CategoryType.SOCIAL,
                points=100,
                icon="🤝",
                unlock_criteria={"referrals": 1}
            ),
            Achievement(
                achievement_id="mentor",
                title="Mentor Master",
                description="Support 5 users in their journey",
                tier=AchievementTier.GOLD,
                category=CategoryType.SOCIAL,
                points=250,
                icon="🎓",
                unlock_criteria={"referrals": 5}
            ),
        ])
        
        achievements.extend([
            Achievement(
                achievement_id="comeback_king",
                title="Phoenix Rising",
                description="Rebuild a 7-day streak after a reset",
                tier=AchievementTier.SILVER,
                category=CategoryType.MASTERY,
                points=100,
                icon="🔥",
                unlock_criteria={"comebacks": 1},
                secret=True
            ),
            Achievement(
                achievement_id="level_ten",
                title="Veteran Guardian",
                description="Reach Level 10",
                tier=AchievementTier.GOLD,
                category=CategoryType.MASTERY,
                points=200,
                icon="🎖️",
                unlock_criteria={"level": 10}
            ),
            Achievement(
                achievement_id="completionist",
                title="Achievement Hunter",
                description="Unlock 25 different achievements",
                tier=AchievementTier.PLATINUM,
                category=CategoryType.MASTERY,
                points=500,
                icon="🏅",
                unlock_criteria={"total_achievements": 25}
            ),
        ])
        
        return achievements
    
    def _calculate_level_thresholds(self) -> Dict[int, int]:
        """Calculate points required for each level (1-100)."""
        
        thresholds = {}
        base_points = 100
        
        for level in range(1, 101):
            points_needed = int(base_points * (1.15 ** (level - 1)))
            thresholds[level] = points_needed
        
        return thresholds
    
    async def check_achievement_unlock(
        self, 
        user_id: str, 
        user_progress: UserProgress
    ) -> List[Achievement]:
        """Check if user has unlocked new achievements."""
        
        newly_unlocked = []
        
        stats = {
            "streak_days": user_progress.current_streak,
            "threats_blocked": user_progress.total_threats_blocked,
            "level": user_progress.level,
            "total_achievements": len(user_progress.achievements_unlocked)
        }
        
        for achievement in self.achievements:
            if achievement.achievement_id in user_progress.achievements_unlocked:
                continue
            
            if self._meets_criteria(achievement.unlock_criteria, stats):
                newly_unlocked.append(achievement)
                user_progress.achievements_unlocked.append(achievement.achievement_id)
                user_progress.total_points += achievement.points
        
        return newly_unlocked
    
    def _meets_criteria(self, criteria: Dict, stats: Dict) -> bool:
        """Check if user stats meet achievement criteria."""
        
        for key, required_value in criteria.items():
            if stats.get(key, 0) < required_value:
                return False
        
        return True
    
    async def calculate_level(self, total_points: int) -> int:
        """Calculate user level based on total points."""
        
        level = 1
        
        for lvl in range(1, 101):
            if total_points >= self.level_thresholds[lvl]:
                level = lvl
            else:
                break
        
        return level
    
    async def get_next_level_progress(
        self, 
        current_points: int, 
        current_level: int
    ) -> Dict:
        """Calculate progress toward next level."""
        
        if current_level >= 100:
            return {
                "current_level": 100,
                "next_level": 100,
                "progress_percent": 100.0,
                "points_needed": 0,
                "max_level_reached": True
            }
        
        current_threshold = self.level_thresholds[current_level]
        next_threshold = self.level_thresholds[current_level + 1]
        
        points_in_level = current_points - current_threshold
        points_needed_for_next = next_threshold - current_threshold
        
        progress = (points_in_level / points_needed_for_next) * 100
        
        return {
            "current_level": current_level,
            "next_level": current_level + 1,
            "progress_percent": round(progress, 1),
            "points_in_this_level": points_in_level,
            "points_needed": points_needed_for_next - points_in_level,
            "max_level_reached": False
        }
    
    async def get_leaderboard(
        self, 
        category: str = "global", 
        timeframe: str = "all_time"
    ) -> List[Dict]:
        """Get leaderboard rankings."""
        
        leaderboard = [
            {"rank": 1, "username": "Guardian_Alpha", "points": 15420, "level": 42, "streak": 156},
            {"rank": 2, "username": "Phoenix_Rising", "points": 12890, "level": 38, "streak": 98},
            {"rank": 3, "username": "SteelWill", "points": 11550, "level": 35, "streak": 112},
            {"rank": 4, "username": "MindfulWarrior", "points": 9870, "level": 32, "streak":  67},
            {"rank": 5, "username": "Resilient_One", "points": 8920, "level": 30, "streak": 81},
        ]
        
        return leaderboard
    
    async def generate_daily_challenge(self, user_level: int) -> Dict:
        """Generate personalized daily challenge based on level."""
        
        import random
        
        challenges = {
            "beginner": [
                {
                    "id": "mindful_moment",
                    "title": "Mindful Moment",
                    "description": "Take 5 minutes for meditation or deep breathing",
                    "points": 25,
                    "difficulty": "easy"
                },
                {
                    "id": "tech_free_hour",
                    "title": "Tech-Free Hour",
                    "description": "Spend 1 hour without screens",
                    "points": 30,
                    "difficulty": "easy"
                },
            ],
            "intermediate": [
                {
                    "id": "outdoor_adventure",
                    "title": "Outdoor Adventure",
                    "description": "Spend 30 minutes outside in nature",
                    "points": 50,
                    "difficulty": "medium"
                },
                {
                    "id": "creative_pursuit",
                    "title": "Creative Expression",
                    "description": "Engage in a creative activity for 20 minutes",
                    "points": 45,
                    "difficulty": "medium"
                },
            ],
            "advanced": [
                {
                    "id": "help_others",
                    "title": "Pay It Forward",
                    "description": "Help or mentor someone else in their journey",
                    "points": 100,
                    "difficulty": "hard"
                },
                {
                    "id": "perfect_day",
                    "title": "Flawless Execution",
                    "description": "Complete the day with zero threats and all wellness goals met",
                    "points": 150,
                    "difficulty": "hard"
                },
            ]
        }
        
        if user_level < 10:
            difficulty = "beginner"
        elif user_level < 30:
            difficulty = "intermediate"
        else:
            difficulty = "advanced"
        
        challenge = random.choice(challenges[difficulty])
        challenge["expires_at"] = (datetime.utcnow() + timedelta(days=1)).isoformat()
        challenge["issued_at"] = datetime.utcnow().isoformat()
        
        return challenge
    
    async def get_rewards_catalog(self) -> List[Dict]:
        """Get available rewards that can be unlocked with points."""
        
        return [
            {
                "reward_id": "custom_theme_1",
                "name": "Cosmic Purple Theme",
                "description": "Unlock a premium app color theme",
                "cost_points": 500,
                "category": "customization",
                "icon": "🎨"
            },
            {
                "reward_id": "trophy_cabinet",
                "name": "Trophy Cabinet",
                "description": "Showcase your achievements on your profile",
                "cost_points": 750,
                "category": "feature",
                "icon": "🏆"
            },
            {
                "reward_id": "mentor_badge",
                "name": "Mentor Badge",
                "description": "Ability to mentor newer users",
                "cost_points": 1000,
                "category": "privilege",
                "icon": "🎓"
            },
            {
                "reward_id": "custom_motivations",
                "name": "Custom Motivational Messages",
                "description": "Create your own motivational messages",
                "cost_points": 300,
                "category": "customization",
                "icon": "💬"
            },
            {
                "reward_id": "analytics_pro",
                "name": "Pro Analytics Dashboard",
                "description": "Unlock advanced analytics and insights",
                "cost_points": 1500,
                "category": "feature",
                "icon": "📊"
            },
        ]
    
    async def redeem_reward(
        self, 
        user_id: str, 
        reward_id: str, 
        user_points: int
    ) -> Dict:
        """Redeem a reward using points."""
        
        catalog = await self.get_rewards_catalog()
        reward = next((r for r in catalog if r["reward_id"] == reward_id), None)
        
        if not reward:
            return {"success": False, "message": "Reward not found"}
        
        if user_points < reward["cost_points"]:
            return {
                "success": False, 
                "message": f"Insufficient points. Need {reward['cost_points']}, have {user_points}"
            }
        
        return {
            "success": True,
            "reward": reward,
            "points_spent": reward["cost_points"],
            "remaining_points": user_points - reward["cost_points"],
            "unlocked_at": datetime.utcnow().isoformat()
        }
    
    async def get_achievement_showcase(
        self, 
        user_id: str, 
        unlocked_achievements: List[str]
    ) -> Dict:
        """Get formatted achievement showcase for profile."""
        
        showcase = {
            "total_unlocked": len(unlocked_achievements),
            "total_available": len(self.achievements),
            "completion_percent": (len(unlocked_achievements) / len(self.achievements)) * 100,
            "by_tier": {"bronze": 0, "silver": 0, "gold": 0, "platinum": 0, "diamond": 0},
            "featured_achievements": [],
            "next_unlock_suggestions": []
        }
        
        for achievement in self.achievements:
            if achievement.achievement_id in unlocked_achievements:
                showcase["by_tier"][achievement.tier.value] += 1
                if achievement.tier in [AchievementTier.PLATINUM, AchievementTier.DIAMOND]:
                    showcase["featured_achievements"].append(asdict(achievement))
        
        return showcase
