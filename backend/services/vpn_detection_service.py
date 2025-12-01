import asyncio
import httpx
import os
from typing import Dict, Optional, List
from datetime import datetime, timedelta

class VPNDetectionService:
    def __init__(self):
        self.iphub_api_key = os.getenv('IPHUB_API_KEY')
        self.cache = {}
        self.cache_duration = timedelta(hours=24)
        
        self.known_vpn_providers = [
            'nordvpn', 'expressvpn', 'surfshark', 'cyberghost', 'privateinternetaccess',
            'protonvpn', 'ipvanish', 'vyprvpn', 'tunnelbear', 'windscribe',
            'purevpn', 'hotspotshield', 'torguard', 'mullvad', 'perfect-privacy'
        ]
        
        self.vpn_port_indicators = [1194, 1723, 500, 4500, 1701]
        
        self.private_ip_ranges = [
            '10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.',
            '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.',
            '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '192.168.'
        ]
    
    async def check_ip(self, ip_address: str) -> Dict:
        if self._is_private_ip(ip_address):
            return {
                'is_vpn': True,
                'confidence': 0.9,
                'method': 'private_ip_range',
                'provider': 'Unknown VPN',
                'details': 'Private IP address detected'
            }
        
        cached = self._get_from_cache(ip_address)
        if cached:
            return cached
        
        result = await self._check_with_iphub(ip_address)
        
        if not result['is_vpn']:
            result = await self._check_with_ipapi(ip_address)
        
        self._save_to_cache(ip_address, result)
        return result
    
    def _is_private_ip(self, ip: str) -> bool:
        return any(ip.startswith(prefix) for prefix in self.private_ip_ranges)
    
    async def _check_with_iphub(self, ip: str) -> Dict:
        if not self.iphub_api_key:
            return {'is_vpn': False, 'confidence': 0.0, 'method': 'iphub_disabled'}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f'https://v2.api.iphub.info/ip/{ip}',
                    headers={'X-Key': self.iphub_api_key},
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    block_status = data.get('block', 0)
                    
                    return {
                        'is_vpn': block_status > 0,
                        'confidence': 0.95 if block_status == 1 else 0.7,
                        'method': 'iphub_api',
                        'provider': data.get('isp', 'Unknown'),
                        'country': data.get('countryCode', 'Unknown'),
                        'details': f"Block status: {block_status}"
                    }
        except Exception as e:
            pass
        
        return {'is_vpn': False, 'confidence': 0.0, 'method': 'iphub_failed'}
    
    async def _check_with_ipapi(self, ip: str) -> Dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f'http://ip-api.com/json/{ip}',
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    isp = data.get('isp', '').lower()
                    org = data.get('org', '').lower()
                    
                    is_vpn = any(provider in isp or provider in org 
                                for provider in self.known_vpn_providers)
                    
                    is_hosting = any(term in isp or term in org 
                                   for term in ['hosting', 'datacenter', 'cloud', 'server'])
                    
                    if is_vpn:
                        return {
                            'is_vpn': True,
                            'confidence': 0.85,
                            'method': 'ipapi_provider_match',
                            'provider': data.get('isp', 'Unknown'),
                            'country': data.get('countryCode', 'Unknown'),
                            'details': f"ISP: {isp}"
                        }
                    elif is_hosting:
                        return {
                            'is_vpn': True,
                            'confidence': 0.6,
                            'method': 'ipapi_hosting_detected',
                            'provider': data.get('isp', 'Unknown'),
                            'country': data.get('countryCode', 'Unknown'),
                            'details': 'Hosting/datacenter IP detected'
                        }
        except Exception as e:
            pass
        
        return {'is_vpn': False, 'confidence': 0.0, 'method': 'ipapi_clean'}
    
    def detect_dns_leak(self, dns_servers: List[str]) -> Dict:
        known_vpn_dns = [
            '103.86.96.100', '103.86.99.100',
            '162.252.172.57', '198.50.200.1',
            '209.222.18.222', '209.222.18.218'
        ]
        
        for dns in dns_servers:
            if dns in known_vpn_dns:
                return {
                    'leak_detected': True,
                    'confidence': 0.9,
                    'dns_server': dns,
                    'details': 'Known VPN DNS server detected'
                }
        
        return {'leak_detected': False, 'confidence': 0.0}
    
    def analyze_connection_timing(self, latency_ms: float, expected_latency_ms: float) -> Dict:
        if latency_ms > expected_latency_ms * 2:
            return {
                'suspicious': True,
                'confidence': 0.7,
                'details': f'High latency detected: {latency_ms}ms vs expected {expected_latency_ms}ms',
                'reason': 'VPN routing overhead suspected'
            }
        
        return {'suspicious': False, 'confidence': 0.0}
    
    def _get_from_cache(self, ip: str) -> Optional[Dict]:
        if ip in self.cache:
            cached_at, result = self.cache[ip]
            if datetime.utcnow() - cached_at < self.cache_duration:
                return result
        return None
    
    def _save_to_cache(self, ip: str, result: Dict):
        self.cache[ip] = (datetime.utcnow(), result)
