import re
import asyncio
from typing import Dict, List, Optional
from datetime import datetime

class DarkWebDetectionService:
    def __init__(self):
        self.onion_pattern = re.compile(r'(?:https?://)?([a-z2-7]{16,56})\.onion', re.IGNORECASE)
        self.i2p_pattern = re.compile(r'(?:https?://)?([a-z0-9\-]+)\.i2p', re.IGNORECASE)
        
        self.dark_web_keywords = [
            'darknet', 'deep web', 'tor browser', 'onion routing',
            'hidden service', 'anonymous network', 'i2p router',
            'freenet', 'zeronet', 'lokinet'
        ]
        
        self.known_onion_sites = [
            'thehiddenwiki',
            'duckduckgo',
            'facebook',
            'torch',
            'ahmia'
        ]
        
        self.dark_web_gateways = [
            'onion.link', 'onion.ly', 'onion.ws', 'tor2web.org',
            'onion.to', 'onion.cab', 'onion.city', 'onion.direct',
            'i2p.rocks', 'i2pd.org'
        ]
        
        self.tor_exit_nodes = set()
        self.last_tor_update = None
    
    def check_url(self, url: str) -> Dict:
        url_lower = url.lower()
        
        onion_match = self.onion_pattern.search(url)
        if onion_match:
            return {
                'is_dark_web': True,
                'confidence': 1.0,
                'type': 'onion_url',
                'network': 'Tor',
                'address': onion_match.group(0),
                'details': 'Direct .onion address detected',
                'severity': 'CRITICAL'
            }
        
        i2p_match = self.i2p_pattern.search(url)
        if i2p_match:
            return {
                'is_dark_web': True,
                'confidence': 1.0,
                'type': 'i2p_url',
                'network': 'I2P',
                'address': i2p_match.group(0),
                'details': 'Direct .i2p address detected',
                'severity': 'CRITICAL'
            }
        
        for gateway in self.dark_web_gateways:
            if gateway in url_lower:
                return {
                    'is_dark_web': True,
                    'confidence': 0.95,
                    'type': 'dark_web_gateway',
                    'network': 'Gateway',
                    'gateway': gateway,
                    'details': f'Dark web gateway detected: {gateway}',
                    'severity': 'HIGH'
                }
        
        for keyword in self.dark_web_keywords:
            if keyword in url_lower:
                return {
                    'is_dark_web': False,
                    'confidence': 0.5,
                    'type': 'keyword_match',
                    'keyword': keyword,
                    'details': f'Dark web keyword detected: {keyword}',
                    'severity': 'MEDIUM'
                }
        
        return {
            'is_dark_web': False,
            'confidence': 0.0,
            'type': 'clean',
            'details': 'No dark web indicators found'
        }
    
    def check_for_tor_browser(self, user_agent: str) -> Dict:
        tor_indicators = [
            'Tor Browser',
            'TorBrowser',
            'Tor/',
            'Mozilla/5.0 (Windows NT 10.0; rv:102.0)',
            'Mozilla/5.0 (Windows NT 10.0; rv:91.0)'
        ]
        
        for indicator in tor_indicators:
            if indicator in user_agent:
                return {
                    'is_tor_browser': True,
                    'confidence': 0.9,
                    'indicator': indicator,
                    'details': 'Tor Browser user agent detected',
                    'severity': 'HIGH'
                }
        
        if 'Firefox' in user_agent and 'Windows NT 10.0' in user_agent:
            firefox_version_match = re.search(r'rv:([\d.]+)', user_agent)
            if firefox_version_match and len(user_agent) < 150:
                return {
                    'is_tor_browser': False,
                    'confidence': 0.6,
                    'details': 'Suspicious Firefox user agent (possible Tor)',
                    'severity': 'MEDIUM'
                }
        
        return {
            'is_tor_browser': False,
            'confidence': 0.0,
            'details': 'No Tor Browser indicators'
        }
    
    async def check_ip_against_tor_exit_nodes(self, ip: str) -> Dict:
        await self._update_tor_exit_nodes()
        
        if ip in self.tor_exit_nodes:
            return {
                'is_tor_exit': True,
                'confidence': 1.0,
                'ip': ip,
                'details': 'IP matches known Tor exit node',
                'severity': 'CRITICAL'
            }
        
        return {
            'is_tor_exit': False,
            'confidence': 0.0,
            'details': 'IP not a known Tor exit node'
        }
    
    async def _update_tor_exit_nodes(self):
        if (self.last_tor_update and 
            (datetime.utcnow() - self.last_tor_update).total_seconds() < 3600):
            return
        
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'https://check.torproject.org/torbulkexitlist',
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    exit_nodes = response.text.strip().split('\n')
                    self.tor_exit_nodes = set(ip.strip() for ip in exit_nodes if ip.strip())
                    self.last_tor_update = datetime.utcnow()
        except:
            pass
    
    def detect_dark_web_ports(self, open_ports: List[int]) -> Dict:
        tor_ports = [9001, 9030, 9050, 9051, 9150, 9151]
        i2p_ports = [4444, 4445, 7656, 7657, 7658]
        
        detected_tor = [port for port in open_ports if port in tor_ports]
        detected_i2p = [port for port in open_ports if port in i2p_ports]
        
        if detected_tor:
            return {
                'dark_web_ports_detected': True,
                'confidence': 0.85,
                'network': 'Tor',
                'ports': detected_tor,
                'details': f'Tor ports detected: {detected_tor}',
                'severity': 'HIGH'
            }
        
        if detected_i2p:
            return {
                'dark_web_ports_detected': True,
                'confidence': 0.85,
                'network': 'I2P',
                'ports': detected_i2p,
                'details': f'I2P ports detected: {detected_i2p}',
                'severity': 'HIGH'
            }
        
        return {
            'dark_web_ports_detected': False,
            'confidence': 0.0,
            'details': 'No dark web ports detected'
        }
    
    def comprehensive_check(self, url: str, ip: str, user_agent: str) -> Dict:
        url_check = self.check_url(url)
        browser_check = self.check_for_tor_browser(user_agent)
        
        is_dangerous = url_check['is_dark_web'] or (
            url_check.get('confidence', 0) > 0.5 and 
            browser_check.get('is_tor_browser', False)
        )
        
        max_confidence = max(
            url_check.get('confidence', 0),
            browser_check.get('confidence', 0)
        )
        
        return {
            'is_dangerous': is_dangerous,
            'overall_confidence': max_confidence,
            'url_analysis': url_check,
            'browser_analysis': browser_check,
            'recommendation': 'BLOCK' if is_dangerous else 'ALLOW',
            'severity': url_check.get('severity', 'LOW')
        }
