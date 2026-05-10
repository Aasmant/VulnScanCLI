"""
Simple Nmap scanner wrapper for network scanning.
"""

import json
from typing import Dict, List, Optional
import nmap


class NmapScanner:
    """Wrapper around nmap for simple network scanning."""
    
    def __init__(self):
        self.nm = nmap.PortScanner()
    
    def scan(self, target: str, ports: Optional[str] = None, timeout: int = 300) -> Dict:
        """
        Scan a target network.
        
        Args:
            target: IP address or CIDR range (e.g., 192.168.1.0/24)
            ports: Port range (e.g., "22,80,443" or "1-1000")
            timeout: Scan timeout in seconds
            
        Returns:
            Dictionary with scan results
        """
        # Build Nmap arguments
        args = '-sn'  # Ping scan by default
        
        if ports:
            args = f'-sV -p {ports}'  # Service version detection
        
        try:
            # Run scan
            self.nm.scan(hosts=target, arguments=args, timeout=timeout)
            
            # Parse results
            results = {
                'target': target,
                'ports': ports or 'ping-scan',
                'hosts': []
            }
            
            for host in self.nm.all_hosts():
                if self.nm[host].state() == 'up':
                    host_info = {
                        'ip': host,
                        'hostname': self.nm[host].hostname() or 'Unknown',
                        'state': self.nm[host].state(),
                        'services': []
                    }
                    
                    # Get open ports/services if version scan was done
                    if 'tcp' in self.nm[host]:
                        for port in self.nm[host]['tcp']:
                            if self.nm[host]['tcp'][port]['state'] == 'open':
                                host_info['services'].append({
                                    'port': port,
                                    'state': self.nm[host]['tcp'][port]['state'],
                                    'service': self.nm[host]['tcp'][port].get('name', 'unknown'),
                                    'version': self.nm[host]['tcp'][port].get('version', '')
                                })
                    
                    results['hosts'].append(host_info)
            
            return results
            
        except nmap.PortScannerError as e:
            raise Exception(f"Nmap scan failed: {e}")
    
    def get_common_vulnerabilities(self, service: str, version: str = '') -> List[Dict]:
        """
        Return common vulnerabilities for a service.
        This is a simple local database, not connected to external APIs.
        
        Args:
            service: Service name (e.g., 'ssh', 'http')
            version: Service version
            
        Returns:
            List of known vulnerabilities
        """
        # Simple local database of common vulnerabilities
        vulns_db = {
            'ssh': [
                {'name': 'Weak SSH Keys', 'severity': 'high', 'cvss': 7.5},
                {'name': 'SSH Brute Force', 'severity': 'medium', 'cvss': 5.5},
            ],
            'http': [
                {'name': 'Unencrypted HTTP', 'severity': 'high', 'cvss': 7.5},
                {'name': 'Missing Security Headers', 'severity': 'medium', 'cvss': 5.5},
            ],
            'ftp': [
                {'name': 'Unencrypted FTP', 'severity': 'high', 'cvss': 8.0},
                {'name': 'Anonymous FTP Access', 'severity': 'medium', 'cvss': 6.5},
            ],
            'telnet': [
                {'name': 'Unencrypted Telnet', 'severity': 'critical', 'cvss': 9.0},
            ],
        }
        
        return vulns_db.get(service.lower(), [])
