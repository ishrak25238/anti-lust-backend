import secrets
import string
import json
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from database import User, IllegalContentAttempt
from services.notification_service import NotificationManager
from services.sms_service import SMSNotificationService

class ParentChildService:
    def __init__(self, db_session):
        self.db = db_session
        self.notifier = NotificationManager()
        self.sms_service = SMSNotificationService()
    
    async def generate_pairing_code(self, parent_email: str) -> str:
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        parent = await self.db.execute(
            "SELECT * FROM users WHERE email = :email",
            {"email": parent_email}
        )
        parent = parent.first()
        if parent:
            parent.pairing_code = code
            await self.db.commit()
        return code
    
    async def pair_child_account(self, child_email: str, pairing_code: str) -> bool:
        parent = await self.db.execute(
            "SELECT * FROM users WHERE pairing_code = :code",
            {"code": pairing_code}
        )
        parent = parent.first()
        if not parent:
            return False
        
        child = await self.db.execute(
            "SELECT * FROM users WHERE email = :email",
            {"email": child_email}
        )
        child = child.first()
        if child:
            child.parent_id = parent.id
            child.parent_email = parent.email
            child.control_mode = 'parent'
            await self.db.commit()
            return True
        return False
    
    async def notify_parent_illegal_content(self, child_id: int, url: str, content_type: str, ai_confidence: float):
        child = await self.db.get(User, child_id)
        if not child or not child.parent_email:
            return
        
        attempt = IllegalContentAttempt(
            user_id=child_id,
            url=url,
            content_type=content_type,
            ai_confidence=ai_confidence,
            timestamp=datetime.utcnow(),
            parent_notified=True,
            session_terminated=True
        )
        self.db.add(attempt)
        await self.db.commit()
        
        await self.notifier.send_notification(
            recipient=child.parent_email,
            type='illegal_content_alert',
            context={
                'child_email': child.email,
                'url': url,
                'content_type': content_type,
                'confidence': f"{ai_confidence*100:.1f}%",
                'timestamp': datetime.utcnow().isoformat()
            }
        )
        
        return True
    
    async def get_child_accounts(self, parent_id: int) -> List[Dict]:
        children = await self.db.execute(
            "SELECT * FROM users WHERE parent_id = :parent_id",
            {"parent_id": parent_id}
        )
        return [
            {
                'id': child.id,
                'email': child.email,
                'emergency_mode': child.emergency_mode,
                'vpn_detected': child.vpn_detected_count > 0,
                'created_at': child.created_at.isoformat()
            }
            for child in children.all()
        ]
    
    async def update_child_permissions(self, parent_id: int, child_id: int, permissions: Dict) -> bool:
        child = await self.db.get(User, child_id)
        if not child or child.parent_id != parent_id:
            return False
        
        if 'allowed_hours_start' in permissions:
            child.allowed_hours_start = permissions['allowed_hours_start']
        if 'allowed_hours_end' in permissions:
            child.allowed_hours_end = permissions['allowed_hours_end']
        if 'blocked_apps' in permissions:
            child.blocked_apps = json.dumps(permissions['blocked_apps'])
        if 'allowed_apps' in permissions:
            child.allowed_apps = json.dumps(permissions['allowed_apps'])
        if 'uninstall_protected' in permissions:
            child.uninstall_protected = permissions['uninstall_protected']
        
        await self.db.commit()
        return True
    
    async def check_time_allowed(self, user_id: int) -> bool:
        user = await self.db.get(User, user_id)
        if not user:
            return False
        
        current_hour = datetime.utcnow().hour
        return user.allowed_hours_start <= current_hour < user.allowed_hours_end
    
    async def check_app_allowed(self, user_id: int, app_package: str) -> bool:
        user = await self.db.get(User, user_id)
        if not user:
            return False
        
        blocked_apps = json.loads(user.blocked_apps)
        allowed_apps = json.loads(user.allowed_apps)
        
        if app_package in blocked_apps:
            return False
        if allowed_apps and app_package not in allowed_apps:
            return False
        return True
    
    async def detect_vpn(self, user_id: int, ip_address: str) -> bool:
        vpn_indicators = [
            '10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.',
            '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.',
            '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '192.168.'
        ]
        
        is_vpn = any(ip_address.startswith(indicator) for indicator in vpn_indicators)
        
        if is_vpn:
            user = await self.db.get(User, user_id)
            if user:
                user.vpn_detected_count += 1
                await self.db.commit()
                
                if user.parent_email and user.vpn_detected_count >= 3:
                    await self.notifier.send_notification(
                        recipient=user.parent_email,
                        type='vpn_detection',
                        context={
                            'child_email': user.email,
                            'detection_count': user.vpn_detected_count,
                            'ip_address': ip_address
                        }
                    )
        
        return is_vpn
    
    async def create_parent_pin(self, parent_id: int, pin: str) -> bool:
        if len(pin) != 6 or not pin.isdigit():
            return False
        
        user = await self.db.get(User, parent_id)
        if not user:
            return False
        
        hashed_pin = bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt())
        user.parent_pin_hash = hashed_pin.decode('utf-8')
        user.pin_created_at = datetime.utcnow()
        await self.db.commit()
        
        if user.parent_phone_number:
            await self.sms_service.send_pin_creation_confirmation(user.parent_phone_number)
        
        return True
    
    async def verify_parent_pin(self, parent_id: int, pin: str) -> bool:
        user = await self.db.get(User, parent_id)
        if not user or not user.parent_pin_hash:
            return False
        
        try:
            return bcrypt.checkpw(pin.encode('utf-8'), user.parent_pin_hash.encode('utf-8'))
        except:
            return False
    
    async def set_app_permission(self, child_id: int, app_package: str, allowed: bool) -> bool:
        child = await self.db.get(User, child_id)
        if not child:
            return False
        
        blocked_apps = json.loads(child.blocked_apps or '[]')
        allowed_apps = json.loads(child.allowed_apps or '[]')
        
        if allowed:
            if app_package in blocked_apps:
                blocked_apps.remove(app_package)
            if app_package not in allowed_apps:
                allowed_apps.append(app_package)
        else:
            if app_package not in blocked_apps:
                blocked_apps.append(app_package)
            if app_package in allowed_apps:
                allowed_apps.remove(app_package)
        
        child.blocked_apps = json.dumps(blocked_apps)
        child.allowed_apps = json.dumps(allowed_apps)
        await self.db.commit()
        return True
    
    async def enable_uninstall_protection(self, child_id: int, enabled: bool = True) -> bool:
        child = await self.db.get(User, child_id)
        if not child:
            return False
        
        child.uninstall_protected = enabled
        await self.db.commit()
        return True
    
    async def send_remote_lock_command(self, child_id: int, duration_minutes: int, reason: str = "Parent initiated") -> Dict:
        child = await self.db.get(User, child_id)
        if not child:
            return {'success': False, 'error': 'Child not found'}
        
        lock_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        child.remote_lock_until = lock_until
        child.remote_lock_reason = reason
        await self.db.commit()
        
        if child.parent_email:
            await self.notifier.send_notification(
                recipient=child.parent_email,
                type='remote_lock_activated',
                context={
                    'child_email': child.email,
                    'duration': duration_minutes,
                    'until': lock_until.isoformat(),
                    'reason': reason
                }
            )
            
            parent = await self.db.get(User, child.parent_id)
            if parent and parent.parent_phone_number:
                await self.sms_service.send_pin_alert(
                    parent.parent_phone_number,
                    'remote_lock',
                    {
                        'duration': duration_minutes,
                        'reason': reason,
                        'child_email': child.email
                    }
                )
        
        return {
            'success': True,
            'lock_until': lock_until.isoformat(),
            'duration_minutes': duration_minutes
        }
    
    async def check_remote_lock_status(self, child_id: int) -> Dict:
        child = await self.db.get(User, child_id)
        if not child:
            return {'is_locked': False}
        
        if child.remote_lock_until and child.remote_lock_until > datetime.utcnow():
            return {
                'is_locked': True,
                'until': child.remote_lock_until.isoformat(),
                'reason': child.remote_lock_reason,
                'remaining_minutes': int((child.remote_lock_until - datetime.utcnow()).total_seconds() / 60)
            }
        
        return {'is_locked': False}
    
    async def unlock_child_device(self, child_id: int) -> bool:
        child = await self.db.get(User, child_id)
        if not child:
            return False
        
        child.remote_lock_until = None
        child.remote_lock_reason = None
        await self.db.commit()
        return True
    
    async def get_app_permissions(self, child_id: int) -> Dict:
        child = await self.db.get(User, child_id)
        if not child:
            return {'blocked_apps': [], 'allowed_apps': []}
        
        return {
            'blocked_apps': json.loads(child.blocked_apps or '[]'),
            'allowed_apps': json.loads(child.allowed_apps or '[]'),
            'uninstall_protected': child.uninstall_protected or False
        }
    
    async def attempt_uninstall(self, child_id: int, pin: str) -> Dict:
        child = await self.db.get(User, child_id)
        if not child:
            return {'allowed': False, 'reason': 'User not found'}
        
        if not child.uninstall_protected:
            return {'allowed': True}
        
        if not child.parent_id:
            return {'allowed': False, 'reason': 'No parent account linked'}
        
        parent = await self.db.get(User, child.parent_id)
        if not parent or not parent.parent_pin_hash:
            return {'allowed': False, 'reason': 'Parent PIN not set'}
        
        pin_valid = await self.verify_parent_pin(child.parent_id, pin)
        
        if pin_valid:
            if parent.email:
                await self.notifier.send_notification(
                    recipient=parent.email,
                    type='app_uninstall_attempt',
                    context={
                        'child_email': child.email,
                        'status': 'ALLOWED',
                        'timestamp': datetime.utcnow().isoformat()
                    }
                )
            if parent.parent_phone_number:
                await self.sms_service.send_pin_alert(
                    parent.parent_phone_number,
                    'uninstall_attempt_allowed',
                    {'child_email': child.email}
                )
            return {'allowed': True}
        else:
            if parent.email:
                await self.notifier.send_notification(
                    recipient=parent.email,
                    type='app_uninstall_attempt',
                    context={
                        'child_email': child.email,
                        'status': 'DENIED - Invalid PIN',
                        'timestamp': datetime.utcnow().isoformat()
                    }
                )
            if parent.parent_phone_number:
                await self.sms_service.send_pin_alert(
                    parent.parent_phone_number,
                    'uninstall_attempt_denied',
                    {
                        'child_email': child.email,
                        'timestamp': datetime.utcnow().isoformat()
                    }
                )
            return {'allowed': False, 'reason': 'Invalid parent PIN'}
