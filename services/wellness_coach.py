"""
Interactive Wellness Coach - AI-powered support system
Provides personalized guidance, motivation, and intervention strategies.
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import random


@dataclass
class CoachMessage:
    message_id: str
    content: str
    category: str
    urgency: str
    timestamp: datetime
    requires_acknowledgment: bool


@dataclass
class WellnessGoal:
    goal_id: str
    title: str
    description: str
    target_value: float
    current_value: float
    deadline: datetime
    status: str
    milestones: List[Dict]


class WellnessCoachAI:
    """Intelligent wellness coach providing personalized support."""
    
    def __init__(self):
        self.message_templates = self._load_message_templates()
        self.intervention_strategies = self._load_intervention_strategies()
        self.motivational_quotes = self._load_motivational_content()
        
    def _load_message_templates(self) -> Dict[str, List[str]]:
        """Load contextual message templates."""
        return {
            "morning_motivation": [
                "Good morning, Commander! A new day brings new victories. Your mission today: stay focused and disciplined.",
                "Rise and shine, Guardian! Yesterday is history, today is your battlefield. Let's conquer it together.",
                "Morning briefing: You've got this! Remember why you started this journey.",
            ],
            "evening_reflection": [
                "Evening debrief: How did today go? Reflect on your victories, no matter how small.",
                "Day complete! Take a moment to acknowledge your  strength and progress.",
                "Mission day ended. Rest well, you've earned it. Tomorrow brings new opportunities.",
            ],
            "streak_milestone": [
                "{days} days strong! You're building incredible mental fortitude.",
                "Achievement unlocked: {days}-day streak! This is the power of consistency.",
                "Milestone reached: {days} days of discipline! You're unstoppable.",
            ],
            "urge_detected": [
                "Alert: I'm sensing vulnerability. Take 5 deep breaths. You're stronger than this urge.",
                "Neural scan detected stress patterns. Engage emergency protocol: Move your body for 2 minutes.",
                "Red alert: This feeling is temporary. Your goals are permanent. Choose wisely.",
            ],
            "progress_celebration": [
                "Analysis complete: Your threat levels have decreased by {percent}%! Outstanding progress!",
                "Data shows remarkable improvement! You're {percent}% better than last week.",
                "Victory detected: You've successfully resisted {count} threats this week!",
            ],
            "encouragement": [
                "You're not alone in this battle. Millions are fighting the same fight.",
                "Every 'no' to temptation is a 'yes' to your future self.",
                "Your brain is rewiring itself right now. Neuroplasticity is on your side.",
            ]
        }
    
    def _load_intervention_strategies(self) -> Dict[str, Dict]:
        """Load evidence-based intervention strategies."""
        return {
            "urge_surfing": {
                "name": "Urge Surfing Technique",
                "duration_seconds": 300,
                "steps": [
                    "Notice the urge without judgment",
                    "Observe its intensity on a scale of 1-10",
                    "Focus on your breath for 5 deep cycles",
                    "Visualize the urge as a wave that rises and falls",
                    "Wait 5 minutes - urges typically peak and fade"
                ],
                "effectiveness_score": 0.85
            },
            "environmental_intervention": {
                "name": "Environment Reset",
                "duration_seconds": 120,
                "steps": [
                    "Stand up immediately",
                    "Move to a different room or go outside",
                    "Change your environment completely",
                    "Engage in a physical activity for 2 minutes",
                    "Return only when feeling centered"
                ],
                "effectiveness_score": 0.78
            },
            "cognitive_reframing": {
                "name": "Thought Challenge",
                "duration_seconds": 180,
                "steps": [
                    "Identify the triggering thought",
                    "Challenge its validity: Is this thought true?",
                    "Consider alternative perspectives",
                    "Replace with a more empowering thought",
                    "Repeat your core motivation statement"
                ],
                "effectiveness_score": 0.82
            },
            "accountability_call": {
                "name": "Reach Out",
                "duration_seconds": 600,
                "steps": [
                    "Text or call your accountability partner",
                    "Be honest about what you're experiencing",
                    "Listen to their support and perspective",
                    "Commit to a specific alternative action",
                    "Follow through immediately"
                ],
                "effectiveness_score": 0.91
            },
            "delayed_gratification": {
                "name": "10-Minute Rule",
                "duration_seconds": 600,
                "steps": [
                    "Set a 10-minute timer",
                    "Engage in ANY different activity",
                    "Don't make the decision until timer ends",
                    "Re-evaluate after 10 minutes",
                    "9 out of 10 times, the urge will have passed"
                ],
                "effectiveness_score": 0.88
            }
        }
    
    def _load_motivational_content(self) -> List[str]:
        """Load motivational quotes and affirmations."""
        return [
            "Your potential is limitless, but it requires daily discipline to unlock.",
            "Every choice is a vote for the person you're becoming.",
            "The pain of discipline far outweighs the pain of regret.",
            "You didn't come this far to only come this far.",
            "Greatness is built in moments when you don't feel like trying.",
            "Your future self is watching you right now.",
            "Progress, not perfection. Focus on the next right choice.",
            "The strongest steel is forged in the hottest fire.",
            "You're rewriting your story one decision at a time.",
            "Champions are made when no one is watching."
        ]
    
    async def get_personalized_coaching(
        self, 
        device_id: str, 
        current_state: Dict
    ) -> CoachMessage:
        """Generate personalized coaching message based on current state."""
        
        hour = datetime.utcnow().hour
        threat_level = current_state.get("threat_level", 0)
        streak_days = current_state.get("streak_days", 0)
        
        if threat_level >= 0.7:
            category = "urge_detected"
            urgency = "high"
            template = random.choice(self.message_templates["urge_detected"])
        elif 6 <= hour < 12:
            category = "morning_motivation"
            urgency = "low"
            template = random.choice(self.message_templates["morning_motivation"])
        elif 20 <= hour < 24:
            category = "evening_reflection"
            urgency = "low"
            template = random.choice(self.message_templates["evening_reflection"])
        elif streak_days > 0 and streak_days % 7 == 0:
            category = "streak_milestone"
            urgency = "medium"
            template = random.choice(self.message_templates["streak_milestone"])
            template = template.format(days=streak_days)
        else:
            category = "encouragement"
            urgency = "low"
            template = random.choice(self.message_templates["encouragement"])
        
        return CoachMessage(
            message_id=f"coach_{datetime.utcnow().timestamp()}",
            content=template,
            category=category,
            urgency=urgency,
            timestamp=datetime.utcnow(),
            requires_acknowledgment=(urgency == "high")
        )
    
    async def recommend_intervention(
        self, 
        threat_level: float, 
        context: Dict
    ) -> Dict:
        """Recommend best intervention strategy based on context."""
        
        if threat_level >= 0.8:
            strategy = self.intervention_strategies["accountability_call"]
        elif threat_level >= 0.6:
            strategy = self.intervention_strategies["urge_surfing"]
        elif threat_level >= 0.4:
            strategy = self.intervention_strategies["environmental_intervention"]
        else:
            strategy = self.intervention_strategies["delayed_gratification"]
        
        return {
            "strategy": strategy,
            "confidence": 0.85,
            "estimated_success_rate": strategy["effectiveness_score"],
            "alternative_strategies": self._get_alternative_strategies(strategy["name"])
        }
    
    def _get_alternative_strategies(self, current: str) -> List[str]:
        """Get alternative intervention strategies."""
        alternatives = [
            name for name in self.intervention_strategies.keys() 
            if name != current
        ]
        return random.sample(alternatives, min(2, len(alternatives)))
    
    async def generate_daily_mission(self, streak_days: int) -> Dict:
        """Generate personalized daily mission/challenge."""
        
        missions = {
            "beginner": [
                {
                    "title": "Awareness Mission",
                    "description": "Notice 3 triggers today without judgment. Just observe.",
                    "reward_points": 10
                },
                {
                    "title": "Environment Scan",
                    "description": "Identify 2 environmental triggers and modify them.",
                    "reward_points": 15
                },
            ],
            "intermediate": [
                {
                    "title": "Urge Practice",
                    "description": "When an urge appears, practice urge surfing for 5 minutes.",
                    "reward_points": 25
                },
                {
                    "title": "Connection Quest",
                    "description": "Reach out to someone you care about. Build real connection.",
                    "reward_points": 20
                },
            ],
            "advanced": [
                {
                    "title": "Mentor Mode",
                    "description": "Share your journey with someone who's struggling. Help them.",
                    "reward_points": 50
                },
                {
                    "title": "Deep Reflection",
                    "description": "Journal for 10 minutes about your growth and future vision.",
                    "reward_points": 35
                },
            ]
        }
        
        if streak_days < 7:
            level = "beginner"
        elif streak_days < 30:
            level = "intermediate"
        else:
            level = "advanced"
        
        mission = random.choice(missions[level])
        mission["level"] = level
        mission["issued_at"] = datetime.utcnow().isoformat()
        mission["expires_at"] = (datetime.utcnow() + timedelta(days=1)).isoformat()
        
        return mission
    
    async def track_wellness_goals(
        self, 
        device_id: str, 
        goals: List[WellnessGoal]
    ) -> Dict:
        """Track progress toward wellness goals."""
        
        summary = {
            "total_goals": len(goals),
            "completed": sum(1 for g in goals if g.status == "completed"),
            "in_progress": sum(1 for g in goals if g.status == "in_progress"),
            "at_risk": sum(1 for g in goals if g.status == "at_risk"),
            "overall_progress": 0.0,
            "recommendations": []
        }
        
        if goals:
            total_progress = sum(
                (g.current_value / g.target_value) if g.target_value > 0 else 0 
                for g in goals
            )
            summary["overall_progress"] = (total_progress / len(goals)) * 100
        
        for goal in goals:
            if goal.deadline < datetime.utcnow() and goal.status != "completed":
                summary["recommendations"].append(
                    f"Goal '{goal.title}' is overdue. Consider revising deadline or breaking into smaller goals."
                )
        
        return summary


class ParentalInsightsDashboard:
    """Advanced dashboard for parents with deep insights and recommendations."""
    
    def __init__(self):
        self.wellness_coach = WellnessCoachAI()
        
    async def generate_weekly_parent_report(
        self, 
        parent_id: str, 
        linked_children: List[str]
    ) -> Dict:
        """Generate comprehensive weekly report for parents."""
        
        report = {
            "report_id": f"parent_weekly_{datetime.utcnow().timestamp()}",
            "parent_id": parent_id,
            "generated_at": datetime.utcnow().isoformat(),
            "period": "past_7_days",
            "children_summaries": [],
            "overall_insights": [],
            "action_items": [],
            "positive_highlights": []
        }
        
        for child_id in linked_children:
            child_summary = await self._generate_child_summary(child_id)
            report["children_summaries"].append(child_summary)
        
        report["overall_insights"] = await self._generate_family_insights(
            report["children_summaries"]
        )
        
        report["action_items"] = await self._generate_parent_action_items(
            report["children_summaries"]
        )
        
        report["positive_highlights"] = self._extract_positive_highlights(
            report["children_summaries"]
        )
        
        return report
    
    async def _generate_child_summary(self, child_id: str) -> Dict:
        """Generate summary for individual child."""
        
        return {
            "child_id": child_id,
            "streak_days": 5,
            "threat_level_trend": "decreasing",
            "total_threats_blocked": 12,
            "screentime_avg_hours": 3.2,
            "peak_vulnerability_hours": [20, 21, 22],
            "notable_improvements": [
                "Responded well to time limits",
                "Reached out for help twice this week"
            ],
            "areas_of_concern": [
                "Late-night usage increasing"
            ],
            "recommended_conversations": [
                "Discuss healthy bedtime routines",
                "Acknowledge their progress this week"
            ]
        }
    
    async def _generate_family_insights(
        self, 
        children_summaries: List[Dict]
    ) -> List[str]:
        """Generate insights across all children."""
        
        insights = [
            "Family-wide pattern detected: Late evening (8-10 PM) shows highest vulnerability.",
            "Positive trend: Overall threat levels down 22% from last week.",
            "Recommendation: Consider implementing family device-free dinner time.",
            "Success story: Guardian Lock interventions were 85% effective this week."
        ]
        
        return insights
    
    async def _generate_parent_action_items(
        self, 
        children_summaries: List[Dict]
    ) -> List[Dict]:
        """Generate actionable items for parents."""
        
        return [
            {
                "priority": "high",
                "title": "Schedule Check-in Conversation",
                "description": "Have a non-judgmental conversation about online challenges.",
                "estimated_time": "15-20 minutes",
                "suggested_approach": "Use 'I noticed' statements, not accusations."
            },
            {
                "priority": "medium",
                "title": "Review Time Limits",
                "description": "Current limits may need adjustment for late evening hours.",
                "estimated_time": "5 minutes",
                "suggested_approach": "Involve child in setting reasonable boundaries."
            },
            {
                "priority": "low",
                "title": "Celebrate Wins",
                "description": "Acknowledge the 5-day streak milestone.",
                "estimated_time": "2 minutes",
                "suggested_approach": "Small reward or verbal affirmation."
            }
        ]
    
    def _extract_positive_highlights(
        self, 
        children_summaries: List[Dict]
    ) -> List[str]:
        """Extract positive moments to celebrate."""
        
        highlights = [
            "🎉 New personal record: 5 consecutive clean days!",
            "💪 Proactive help-seeking: Child reached out twice this week",
            "📉 Threat levels decreased 35% compared to last week",
            "🏆 100% Guardian Lock compliance - no override attempts"
        ]
        
        return highlights
    
    async def generate_conversation_starters(
        self, 
        child_behavior_summary: Dict
    ) -> List[str]:
        """Generate conversation starters for parent-child discussions."""
        
        starters = [
            "I've noticed you've been doing really well this week. What's been helping you?",
            "Can we talk about what makes late evenings challenging for you?",
            "I'm proud of your progress. What goals do you want to set for next week?",
            "If you could change one thing about the current system, what would it be?",
            "What can I do to better support you in this journey?"
        ]
        
        return starters
    
    async def get_expert_resources(self, concern_category: str) -> Dict:
        """Provide expert resources for parents."""
        
        resources = {
            "addiction_concerns": {
                "articles": [
                    "Understanding Digital Addiction in Teens - Psychology Today",
                    "Neuroplasticity and Recovery - Harvard Medical",
                ],
                "videos": [
                    "The Brain Science of Addiction - TEDx Talk"
                ],
                "professionals": [
                    "Find a therapist: PsychologyToday.com/therapists",
                    "National Helpline: 1-800-662-HELP"
                ]
            },
            "communication_tips": {
                "articles": [
                    "How to Talk to Teens About Difficult Topics - AAP",
                    "Non-Judgmental Communication Strategies"
                ],
                "books": [
                    "'How to Talk So Teens Will Listen' - Adele Faber"
                ]
            }
        }
        
        return resources.get(concern_category, {"message": "General support available at support@antilustguardian.com"})
