"""
VPN Bypass Prevention Service
Detects and blocks VPN/proxy attempts to ensure filtering cannot be bypassed
"""
from services.vpn_detection_service import VPNDetectionService
from services.notification_service import NotificationService
import asyncio

class VPNBypassPrevention:
    def __init__(self):
        self.vpn_detector = VPNDetectionService()
        self.notification_service = NotificationService()
        self.blocked_vpn_providers = [
            'nordvpn', 'expressvpn', 'surfshark', 'protonvpn', 'cyberghost',
            'tunnelbear', 'hidemyass', 'ipvanish', 'purevpn', 'vypr',
            'windscribe', 'hotspotshield', 'privateinternetaccess', 'mullvad'
        ]
    
    async def check_and_block_vpn(self, ip_address: str, device_id: str, parent_email: str = None) -> dict:
        """
        Check if IP is from VPN/proxy and block if detected
        Returns: {is_vpn: bool, blocked: bool, vpn_provider: str}
        """
        # Check IP against VPN detection
        vpn_result = await self.vpn_detector.check_ip(ip_address)
        
        if vpn_result.get('is_vpn') or vpn_result.get('is_proxy'):
            # VPN/Proxy detected - block and notify
            provider =  vpn_result.get('provider', 'Unknown VPN')
            
            # Send alert to parent
            if parent_email:
                await self.notification_service.send_critical_alert(
                    device_id=device_id,
                    parent_email=parent_email,
                    event_type='VPN_BYPASS_ATTEMPT',
                    threat_level='CRITICAL',
                    confidence=vpn_result.get('confidence', 1.0),
                    context={
                        'ip': ip_address,
                        'vpn_provider': provider,
                        'message': f'Child attempted to bypass filtering using {provider}'
                    }
                )
            
            return {
                'is_vpn': True,
                'blocked': True,
                'vpn_provider': provider,
                'action': 'BLOCK_ALL_TRAFFIC',
                'message': 'VPN detected. All traffic blocked until VPN is disabled.',
                'solutions': [
                    'Disable VPN/proxy on device',
                    'Contact parent/guardian for assistance',
                    'VPN apps will be reported to parent'
                ]
            }
        
        return {'is_vpn': False, 'blocked': False}
    
    def is_vpn_app_installed(self, app_package: str) -> bool:
        """Check if package name matches known VPN apps"""
        app_lower = app_package.lower()
        return any(vpn in app_lower for vpn in self.blocked_vpn_providers)
    
    async def block_vpn_apps(self, device_id: str, installed_apps: list, parent_email: str = None):
        """
        Check installed apps and block VPN applications
        """
        blocked_apps = []
        
        for app in installed_apps:
            if self.is_vpn_app_installed(app['package']):
                blocked_apps.append(app)
                
                # Notify parent
                if parent_email:
                    await self.notification_service.send_critical_alert(
                        device_id=device_id,
                        parent_email=parent_email,
                        event_type='VPN_APP_DETECTED',
                        threat_level='HIGH',
                        confidence=1.0,
                        context={
                            'app_name': app.get('name'),
                            'package': app['package'],
                            'message': f"VPN app detected: {app.get('name')}"
                        }
                    )
        
        return {
            'vpn_apps_found': len(blocked_apps),
            'blocked_apps': blocked_apps,
            'action_required': 'UNINSTALL_VPN_APPS' if blocked_apps else None
        }

# Global instance
vpn_bypass_prevention = VPNBypassPrevention()
