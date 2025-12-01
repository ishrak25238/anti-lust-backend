import re
import socket
import struct
from typing import Optional, Dict, List
import requests

class SecurityService:
    def __init__(self):
        self.vpn_ip_ranges = self._load_vpn_ranges()
        self.tor_exit_nodes = self._load_tor_nodes()
        self.onion_pattern = re.compile(r'\.onion$')
    
    def _load_vpn_ranges(self) -> List[str]:
        return [
            '10.0.0.0/8',
            '172.16.0.0/12',
            '192.168.0.0/16',
            '100.64.0.0/10'
        ]
    
    def _load_tor_nodes(self) -> set:
        try:
            response = requests.get('https://check.torproject.org/torbulkexitlist', timeout=5)
            if response.status_code == 200:
                return set(response.text.strip().split('\n'))
        except:
            pass
        return set()
    
    def detect_vpn(self, ip_address: str) -> Dict[str, any]:
        if self._is_private_ip(ip_address):
            return {'is_vpn': True, 'confidence': 0.9, 'reason': 'Private IP range'}
        
        if ip_address in self.tor_exit_nodes:
            return {'is_vpn': True, 'confidence': 1.0, 'reason': 'Tor exit node'}
        
        if self._check_vpn_api(ip_address):
            return {'is_vpn': True, 'confidence': 0.85, 'reason': 'VPN detected by API'}
        
        return {'is_vpn': False, 'confidence': 0.0, 'reason': 'No VPN detected'}
    
    def _is_private_ip(self, ip: str) -> bool:
        try:
            ip_int = struct.unpack('!I', socket.inet_aton(ip))[0]
            
            private_ranges = [
                (struct.unpack('!I', socket.inet_aton('10.0.0.0'))[0], 
                 struct.unpack('!I', socket.inet_aton('10.255.255.255'))[0]),
                (struct.unpack('!I', socket.inet_aton('172.16.0.0'))[0], 
                 struct.unpack('!I', socket.inet_aton('172.31.255.255'))[0]),
                (struct.unpack('!I', socket.inet_aton('192.168.0.0'))[0], 
                 struct.unpack('!I', socket.inet_aton('192.168.255.255'))[0]),
            ]
            
            for start, end in private_ranges:
                if start <= ip_int <= end:
                    return True
            return False
        except:
            return False
    
    def _check_vpn_api(self, ip: str) -> bool:
        try:
            response = requests.get(f'https://vpnapi.io/api/{ip}', timeout=3)
            if response.status_code == 200:
                data = response.json()
                return data.get('security', {}).get('vpn', False)
        except:
            pass
        return False
    
    def detect_tor_browser(self, user_agent: str) -> bool:
        tor_indicators = ['tor browser', 'torbrowser', 'tor-enabled']
        return any(indicator in user_agent.lower() for indicator in tor_indicators)
    
    def is_onion_domain(self, url: str) -> bool:
        return bool(self.onion_pattern.search(url.lower()))
    
    def detect_proxy(self, headers: Dict[str, str]) -> bool:
        proxy_headers = ['via', 'x-forwarded-for', 'forwarded', 'x-real-ip']
        return any(header.lower() in [h.lower() for h in headers.keys()] for header in proxy_headers)
    
    def check_dns_leak(self, dns_servers: List[str]) -> bool:
        known_vpn_dns = [
            '1.1.1.1', '1.0.0.1',
            '9.9.9.9', '149.112.112.112',
            '8.26.56.26', '8.20.247.20'
        ]
        
        for dns in dns_servers:
            if dns in known_vpn_dns:
                return True
        return False
    
    def get_security_score(self, checks: Dict[str, bool]) -> float:
        weights = {
            'vpn': 0.3,
            'tor': 0.3,
            'proxy': 0.2,
            'dns_leak': 0.2
        }
        
        score = 0.0
        for check, detected in checks.items():
            if detected and check in weights:
                score += weights[check]
        
        return 1.0 - score

class UninstallProtectionService:
    def __init__(self, db_session):
        self.db = db_session
    
    async def request_uninstall_permission(self, user_id: int, entered_pin: str) -> Dict[str, any]:
        from database import User
        import bcrypt
        
        user = await self.db.get(User, user_id)
        if not user:
            return {'allowed': False, 'reason': 'User not found'}
        
        if user.control_mode == 'self':
            if not user.pin_hash:
                return {'allowed': True, 'reason': 'No PIN set'}
            
            if bcrypt.checkpw(entered_pin.encode(), user.pin_hash.encode()):
                return {'allowed': True, 'reason': 'Correct PIN'}
            else:
                return {'allowed': False, 'reason': 'Incorrect PIN'}
        
        elif user.control_mode == 'parent':
            if not user.parent_id:
                return {'allowed': False, 'reason': 'Parent not linked'}
            
            parent = await self.db.get(User, user.parent_id)
            if not parent or not parent.pin_hash:
                return {'allowed': False, 'reason': 'Parent PIN not set'}
            
            if bcrypt.checkpw(entered_pin.encode(), parent.pin_hash.encode()):
                await self._notify_parent_uninstall(user, parent)
                return {'allowed': True, 'reason': 'Parent PIN correct'}
            else:
                await self._log_failed_uninstall_attempt(user)
                return {'allowed': False, 'reason': 'Incorrect parent PIN'}
        
        return {'allowed': False, 'reason': 'Unknown control mode'}
    
    async def _notify_parent_uninstall(self, child: 'User', parent: 'User'):
        from services.notification_service import NotificationManager
        
        notifier = NotificationManager()
        await notifier.send_notification(
            recipient=parent.email,
            type='uninstall_attempt',
            context={
                'child_email': child.email,
                'timestamp': str(datetime.utcnow()),
                'status': 'Approved with parent PIN'
            }
        )
    
    async def _log_failed_uninstall_attempt(self, user: 'User'):
        from services.notification_service import NotificationManager
        
        if user.parent_id:
            parent = await self.db.get(User, user.parent_id)
            if parent:
                notifier = NotificationManager()
                await notifier.send_notification(
                    recipient=parent.email,
                    type='failed_uninstall_attempt',
                    context={
                        'child_email': user.email,
                        'timestamp': str(datetime.utcnow()),
                        'status': 'Blocked - Incorrect PIN'
                    }
                )
    
    def get_required_permissions(self) -> List[str]:
        return [
            'BIND_DEVICE_ADMIN',
            'REQUEST_DELETE_PACKAGES',
            'PACKAGE_USAGE_STATS',
            'QUERY_ALL_PACKAGES'
        ]
