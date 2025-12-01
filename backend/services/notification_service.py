
import logging
import asyncio
import json
import time
import uuid
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timedelta
from collections import deque, defaultdict

from services.notification_data import NotificationTemplates, Template
from services.notification_providers import (
    ProviderConfig, SendGridProvider, AWSSESProvider, SMTPProvider,
    TwilioProvider, MessageBirdProvider,
    DiscordProvider, SlackProvider, TelegramProvider,
    FCMProvider
)
from services.pattern_storage import PatternStorage

logger = logging.getLogger("AntiLustNotificationService")


class NotificationPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

class NotificationType(Enum):
    THREAT_BLOCKED = "threat_blocked"
    TIME_LIMIT = "time_limit"
    SYSTEM_ALERT = "system_alert"
    WEEKLY_REPORT = "weekly_report"
    ACHIEVEMENT = "achievement"
    ACCOUNT_ALERT = "account_alert"

class DeliveryStatus(Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRIED = "retried"

@dataclass
class NotificationContext:
    id: str
    device_id: str
    recipient: str
    priority: NotificationPriority
    notification_type: NotificationType
    language: str = "en"
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    retry_count: int = 0
    max_retries: int = 3
    channels: List[str] = field(default_factory=lambda: ["email"])
    status: DeliveryStatus = DeliveryStatus.PENDING
    error_log: List[str] = field(default_factory=list)


class NotificationAnalytics:
    """
    Real-time analytics engine for notification delivery metrics.
    Tracks success rates, latency, and volume per type/channel.
    """
    
    def __init__(self):
        self.sent_count = 0
        self.failed_count = 0
        self.retry_count = 0
        self.latency_samples = deque(maxlen=1000)
        self.type_counts = defaultdict(int)
        self.channel_counts = defaultdict(int)
        self.hourly_volume = defaultdict(int)
        self.start_time = time.time()

    def log_success(self, context: NotificationContext, latency_ms: float, channel: str):
        self.sent_count += 1
        self.latency_samples.append(latency_ms)
        self.type_counts[context.notification_type.value] += 1
        self.channel_counts[channel] += 1
        
        hour_key = datetime.now().strftime("%Y-%m-%d %H:00")
        self.hourly_volume[hour_key] += 1

    def log_failure(self, context: NotificationContext, channel: str):
        self.failed_count += 1
        self.channel_counts[f"{channel}_failed"] += 1

    def log_retry(self):
        self.retry_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        total = self.sent_count + self.failed_count
        success_rate = (self.sent_count / total * 100) if total > 0 else 0.0
        avg_latency = sum(self.latency_samples) / len(self.latency_samples) if self.latency_samples else 0.0
        
        return {
            "uptime_seconds": time.time() - self.start_time,
            "total_processed": total,
            "sent": self.sent_count,
            "failed": self.failed_count,
            "retried": self.retry_count,
            "success_rate": round(success_rate, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "breakdown_by_type": dict(self.type_counts),
            "breakdown_by_channel": dict(self.channel_counts),
            "hourly_volume": dict(self.hourly_volume)
        }


class NotificationHistory:
    """
    In-memory database for notification history with complex query capabilities.
    """
    
    def __init__(self, max_size: int = 10000):
        self.history: deque[NotificationContext] = deque(maxlen=max_size)
        self.by_device: Dict[str, List[NotificationContext]] = defaultdict(list)
        self.by_id: Dict[str, NotificationContext] = {}

    def add(self, context: NotificationContext):
        self.history.append(context)
        self.by_device[context.device_id].append(context)
        self.by_id[context.id] = context
        
        if len(self.by_device[context.device_id]) > 100:
            self.by_device[context.device_id].pop(0)

    def query(self, 
              device_id: Optional[str] = None, 
              start_time: Optional[float] = None, 
              end_time: Optional[float] = None,
              status: Optional[DeliveryStatus] = None,
              priority: Optional[NotificationPriority] = None,
              limit: int = 50) -> List[Dict]:
        
        results = []
        source = self.by_device[device_id] if device_id else self.history
        
        count = 0
        for ctx in reversed(source):
            if count >= limit:
                break
                
            if start_time and ctx.timestamp < start_time:
                continue
            if end_time and ctx.timestamp > end_time:
                continue
            if status and ctx.status != status:
                continue
            if priority and ctx.priority != priority:
                continue
                
            results.append(asdict(ctx))
            count += 1
            
        return results


class LocalizationManager:
    """
    Manages language detection and preference resolution.
    """
    def __init__(self):
        self.supported_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'jp', 'cn', 'kr', 'ar', 'hi']
        self.default_language = 'en'

    def detect_language(self, context: Dict) -> str:
        if 'language' in context:
            return context['language']
        if 'locale' in context:
            lang = context['locale'].split('-')[0]
            if lang in self.supported_languages:
                return lang
        return self.default_language

class UserPreferences:
    """
    Manages user notification preferences (DND, Channel selection).
    """
    def __init__(self):
        self.preferences: Dict[str, Dict] = defaultdict(lambda: {
            "dnd_enabled": False,
            "dnd_start": "22:00",
            "dnd_end": "07:00",
            "channels": ["email", "push"],
            "min_priority": NotificationPriority.NORMAL.value
        })

    def get_preferences(self, user_id: str) -> Dict:
        return self.preferences[user_id]

    def is_dnd_active(self, user_id: str) -> bool:
        prefs = self.preferences[user_id]
        if not prefs['dnd_enabled']:
            return False
            
        now = datetime.now().time()
        start = datetime.strptime(prefs['dnd_start'], "%H:%M").time()
        end = datetime.strptime(prefs['dnd_end'], "%H:%M").time()
        
        if start < end:
            return start <= now <= end
        else:
            return now >= start or now <= end

    def should_send(self, user_id: str, priority: NotificationPriority) -> bool:
        prefs = self.preferences[user_id]
        if priority.value < prefs['min_priority']:
            return False
        if self.is_dnd_active(user_id) and priority != NotificationPriority.CRITICAL:
            return False
        return True

class BatchProcessor:
    """
    Groups low-priority notifications into a single digest.
    """
    def __init__(self):
        self.batches: Dict[str, List[NotificationContext]] = defaultdict(list)
        self.batch_size = 10
        self.flush_interval = 300

    def add(self, context: NotificationContext) -> bool:
        if context.priority == NotificationPriority.LOW:
            self.batches[context.recipient].append(context)
            return True
        return False

    def get_ready_batches(self) -> List[Tuple[str, List[NotificationContext]]]:
        ready = []
        for recipient, items in self.batches.items():
            if len(items) >= self.batch_size:
                ready.append((recipient, items))
                self.batches[recipient] = []
        return ready

class NotificationScheduler:
    """
    Schedules notifications for future delivery.
    """
    def __init__(self):
        self.scheduled: List[Tuple[float, NotificationContext]] = []

    def schedule(self, context: NotificationContext, delay_seconds: float):
        deliver_at = time.time() + delay_seconds
        self.scheduled.append((deliver_at, context))
        self.scheduled.sort(key=lambda x: x[0])

    def get_due(self) -> List[NotificationContext]:
        now = time.time()
        due = []
        while self.scheduled and self.scheduled[0][0] <= now:
            due.append(self.scheduled.pop(0)[1])
        return due


class RateLimiter:
    """Token Bucket Rate Limiter."""
    def __init__(self, max_tokens: int, refill_rate: float):
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.refill_rate = refill_rate
        self.last_update = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self) -> bool:
        async with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            self.tokens = min(self.max_tokens, self.tokens + elapsed * self.refill_rate)
            self.last_update = now
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

class NotificationManager:
    """
    Orchestrates the entire notification pipeline.
    """
    
    def __init__(self):
        self.templates = NotificationTemplates()
        self.analytics = NotificationAnalytics()
        self.history = NotificationHistory()
        self.queue = asyncio.PriorityQueue()
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.processing = False
        
        self.scheduler = NotificationScheduler()
        self.batcher = BatchProcessor()
        self.preferences = UserPreferences()
        self.localizer = LocalizationManager()
        
        self.providers = {
            'email': SendGridProvider(ProviderConfig(api_key="SG.mock")), # Mock key
            'sms': TwilioProvider(ProviderConfig(api_key="ACmock", api_secret="mock", sender_id="+1555")),
            'discord': DiscordProvider(ProviderConfig(webhook_url="https://discord.com/api/webhooks/mock")),
            'push': FCMProvider(ProviderConfig(api_key="mock_fcm"))
        }

    def _get_rate_limiter(self, device_id: str) -> RateLimiter:
        if device_id not in self.rate_limiters:
            self.rate_limiters[device_id] = RateLimiter(max_tokens=5, refill_rate=1.0/60.0)
        return self.rate_limiters[device_id]

    async def enqueue(self, context: NotificationContext):
        if not self.preferences.should_send(context.recipient, context.priority):
            logger.info(f"Notification suppressed by preferences for {context.recipient}")
            context.status = DeliveryStatus.SKIPPED
            self.history.add(context)
            return

        if self.batcher.add(context):
            logger.info(f"Notification batched for {context.recipient}")
            return

        context.language = self.localizer.detect_language(context.metadata)

        prio_map = {
            NotificationPriority.CRITICAL: 0,
            NotificationPriority.HIGH: 1,
            NotificationPriority.NORMAL: 2,
            NotificationPriority.LOW: 3
        }
        score = prio_map.get(context.priority, 2)
        
        await self.queue.put((score, context))
        
        if not self.processing:
            asyncio.create_task(self._process_queue())

    async def _process_queue(self):
        self.processing = True
        while not self.queue.empty():
            priority_score, context = await self.queue.get()
            
            limiter = self._get_rate_limiter(context.device_id)
            if not await limiter.acquire() and context.priority != NotificationPriority.CRITICAL:
                logger.warning(f"Rate limit hit for {context.device_id}. Re-queueing.")
                await asyncio.sleep(5)
                await self.queue.put((priority_score, context))
                self.queue.task_done()
                continue
            
            await self._deliver(context)
            self.queue.task_done()
            
        self.processing = False

    async def _deliver(self, context: NotificationContext):
        start_time = time.time()
        
        template = self.templates.get_template(context.language, context.notification_type.value)
        if not template:
            logger.error(f"Template not found for {context.notification_type} in {context.language}")
            context.status = DeliveryStatus.FAILED
            context.error_log.append("Template missing")
            self.history.add(context)
            self.analytics.log_failure(context, "template_engine")
            return

        fmt_data = {
            **context.metadata,
            "device_id": context.device_id,
            "timestamp": datetime.fromtimestamp(context.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            "dashboard_link": "https://antilust.com/dashboard"
        }
        
        try:
            subject = template.subject.format(**fmt_data)
            body_html = template.body_html.format(**fmt_data)
            body_text = template.body_text.format(**fmt_data)
        except KeyError as e:
            logger.error(f"Template formatting error: {e}")
            context.status = DeliveryStatus.FAILED
            context.error_log.append(f"Formatting error: {e}")
            self.history.add(context)
            return

        success_any = False
        for channel_name in context.channels:
            provider = self.providers.get(channel_name)
            if not provider or not provider.is_configured():
                continue
                
            try:
                content = body_html if channel_name == 'email' else body_text
                
                success = await provider.send(context.recipient, subject, content, context.metadata)
                
                if success:
                    success_any = True
                    latency = (time.time() - start_time) * 1000
                    self.analytics.log_success(context, latency, channel_name)
                    logger.info(f"Sent {context.notification_type} to {context.recipient} via {channel_name}")
                else:
                    self.analytics.log_failure(context, channel_name)
                    context.error_log.append(f"{channel_name} failed")
                    
            except Exception as e:
                logger.error(f"Provider error {channel_name}: {e}")
                context.error_log.append(f"{channel_name} error: {str(e)}")

        if not success_any:
            if context.retry_count < context.max_retries:
                context.retry_count += 1
                self.analytics.log_retry()
                delay = 2 ** context.retry_count
                logger.info(f"All channels failed. Retrying in {delay}s...")
                await asyncio.sleep(delay)
                await self.enqueue(context)
                return
            else:
                context.status = DeliveryStatus.FAILED
        else:
            context.status = DeliveryStatus.SENT

        self.history.add(context)


class NotificationService:
    """
    Main entry point for the application.
    """
    
    def __init__(self):
        self.manager = NotificationManager()
        
    async def send_critical_alert(self, device_id: str, parent_email: str, 
                                event_type: str, threat_level: str, 
                                confidence: float, context: Dict):
        """
        Sends a critical alert for blocked threats.
        """
        ctx = NotificationContext(
            id=str(uuid.uuid4()),
            device_id=device_id,
            recipient=parent_email,
            priority=NotificationPriority.CRITICAL,
            notification_type=NotificationType.THREAT_BLOCKED,
            language="en", # Could be inferred from user settings
            metadata={
                "event_type": event_type,
                "threat_level": threat_level,
                "confidence": int(confidence * 100),
                **context
            },
            channels=["email", "push"] # Multi-channel for critical
        )
        await self.manager.enqueue(ctx)

    async def send_time_limit_alert(self, device_id: str, parent_email: str, 
                                   category: str, limit: int):
        """
        Sends a time limit alert.
        """
        ctx = NotificationContext(
            id=str(uuid.uuid4()),
            device_id=device_id,
            recipient=parent_email,
            priority=NotificationPriority.HIGH,
            notification_type=NotificationType.TIME_LIMIT,
            metadata={
                "category": category,
                "limit": limit
            },
            channels=["email", "sms"]
        )
        await self.manager.enqueue(ctx)

    def get_analytics(self) -> Dict:
        return self.manager.analytics.get_metrics()

    def get_history(self, device_id: str) -> List[Dict]:
        return self.manager.history.query(device_id=device_id)
