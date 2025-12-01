import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
import json
from collections import deque
import psutil
import time

@dataclass
class DashboardMetric:
    metric_id: str
    name: str
    value: float
    unit: str
    trend: str
    last_updated: datetime
    alert_threshold: Optional[float] = None

@dataclass
class LiveAlert:
    alert_id: str
    severity: str
    title: str
    message: str
    timestamp: datetime
    acknowledged: bool = False
    action_required: bool = False

class RealtimeDashboardService:
    def __init__(self):
        self.active_connections: Set[str] = set()
        self.metrics_buffer = deque(maxlen=1000)
        self.alerts_buffer = deque(maxlen=100)
        self.subscription_topics: Dict[str, Set[str]] = {}
        self.start_time = time.time()
        self.request_count = 0
        
    async def subscribe_to_metrics(self, connection_id: str, topics: List[str]) -> Dict:
        self.active_connections.add(connection_id)
        for topic in topics:
            if topic not in self.subscription_topics:
                self.subscription_topics[topic] = set()
            self.subscription_topics[topic].add(connection_id)
        return {
            "status": "subscribed",
            "connection_id": connection_id,
            "topics": topics,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_live_metrics_snapshot(self, device_id: str) -> Dict:
        from .pattern_storage import PatternStorage
        storage = PatternStorage()
        
        recent_events = storage.get_recent_events(device_id, hours=24)
        threats_today = len([e for e in recent_events if e.get('event_type') == 'threat_detected'])
        
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        metrics = {
            "device_status": {
                "online": True,
                "last_seen": datetime.utcnow().isoformat(),
                "battery_level": 78,
                "signal_strength": "strong"
            },
            "protection_status": {
                "active_filters": 5,
                "threats_blocked_today": threats_today,
                "vpn_detected": False,
                "guardian_lock_active": False
            },
            "behavioral_metrics": {
                "current_threat_level": 0.15,
                "streak_days": 5,
                "screentime_today_minutes": 142,
                "peak_hour_today": 20
            },
            "system_health": {
                "ml_models_loaded": True,
                "database_connected": True,
                "sync_status": "synced",
                "last_backup": (datetime.utcnow() - timedelta(hours=2)).isoformat()
            },
            "realtime_stats": {
                "requests_per_minute": self.request_count,
                "avg_response_time_ms": 45,
                "cache_hit_rate": 0.85,
                "active_sessions": len(self.active_connections),
                "cpu_usage_percent": cpu_percent,
                "memory_usage_mb": memory.used // (1024 * 1024)
            }
        }
        self.request_count += 1
        return metrics
    
    async def stream_metrics_update(self, device_id: str, metric_type: str) -> DashboardMetric:
        from .pattern_storage import PatternStorage
        storage = PatternStorage()
        
        if metric_type == "threat_level":
            recent_threats = storage.get_recent_events(device_id, hours=1)
            threat_count = len([e for e in recent_threats if e.get('event_type') == 'threat_detected'])
            value = min(threat_count / 10.0, 1.0)
            trend = "stable" if threat_count < 5 else "increasing"
            
            return DashboardMetric(
                f"{device_id}_threat_{datetime.utcnow().timestamp()}",
                "Current Threat Level",
                value,
                "score",
                trend,
                datetime.utcnow(),
                0.7
            )
        elif metric_type == "screentime":
            screen_minutes = 180
            return DashboardMetric(
                f"{device_id}_screen_{datetime.utcnow().timestamp()}",
                "Screen Time Today",
                screen_minutes,
                "minutes",
                "increasing",
                datetime.utcnow(),
                300
            )
        else:
            threats_blocked = storage.count_events(device_id, event_type="threat_blocked")
            return DashboardMetric(
                f"{device_id}_blocked_{datetime.utcnow().timestamp()}",
                "Threats Blocked",
                threats_blocked,
                "count",
                "stable",
                datetime.utcnow(),
                None
            )
    
    async def generate_live_alert(self, device_id: str, alert_type: str, context: Dict) -> LiveAlert:
        alert_templates = {
            "high_threat": {
                "severity": "critical",
                "title": "High Threat Detected",
                "message": f"Device {device_id} triggered high-severity content filter. Immediate attention recommended.",
                "action_required": True
            },
            "vpn_detected": {
                "severity": "warning",
                "title": "VPN Usage Detected",
                "message": f"VPN connection detected on device {device_id}. This may indicate bypass attempt.",
                "action_required": True
            },
            "streak_broken": {
                "severity": "info",
                "title": "Streak Reset",
                "message": f"Clean streak was reset on device {device_id}. Encourage and support recovery.",
                "action_required": False
            },
            "milestone_reached": {
                "severity": "success",
                "title": "Milestone Achieved!",
                "message": f"Device {device_id} reached a new milestone: {context.get('milestone', 'Unknown')}!",
                "action_required": False
            },
            "system_error": {
                "severity": "error",
                "title": "System Error",
                "message": f"Technical issue detected on device {device_id}. System administrators notified.",
                "action_required": False
            }
        }
        template = alert_templates.get(alert_type, alert_templates["system_error"])
        return LiveAlert(
            f"alert_{datetime.utcnow().timestamp()}",
            template["severity"],
            template["title"],
            template["message"],
            datetime.utcnow(),
            False,
            template["action_required"]
        )
    
    async def collect_performance_metrics(self) -> Dict:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net_io = psutil.net_io_counters()
        
        elapsed = time.time() - self.start_time
        throughput_mbps = (net_io.bytes_sent + net_io.bytes_recv) / (1024 * 1024) / max(elapsed, 1)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "api_metrics": {
                "requests_per_second": self.request_count / max(elapsed, 1),
                "avg_response_time_ms": 45,
                "error_rate": 0.001,
                "success_rate": 0.999
            },
            "ml_metrics": {
                "model_load_time_ms": 800,
                "inference_time_ms": 95,
                "models_active": 2,
                "cache_hit_rate": 0.85
            },
            "database_metrics": {
                "connection_pool_size": 10,
                "active_connections": len(self.active_connections),
                "query_time_avg_ms": 12,
                "table_sizes_mb": {
                    "events": 245.3,
                    "users": 12.8,
                    "patterns": 89.4
                }
            },
            "system_resources": {
                "cpu_usage_percent": cpu_percent,
                "memory_usage_mb": memory.used // (1024 * 1024),
                "disk_usage_percent": disk.percent,
                "network_throughput_mbps": throughput_mbps
            }
        }
