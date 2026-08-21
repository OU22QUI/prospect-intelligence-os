"""
Layer 3: Network Infrastructure & Shodan InternetDB Scanner
Resolves A/AAAA IP addresses, reverse DNS, and queries the free, keyless Shodan InternetDB endpoint
for open ports, vulnerabilities (CVEs), CPEs, and hostnames.
"""
import socket
import httpx
from typing import Dict, Any, List

class NetworkInfraScanner:
    def __init__(self, timeout: float = 4.0):
        self.timeout = timeout

    def scan(self, domain: str) -> Dict[str, Any]:
        domain = domain.strip().lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        
        result = {
            "domain": domain,
            "ip_addresses": [],
            "reverse_dns": [],
            "open_ports": [],
            "cpes": [],
            "vulns": [],
            "hostnames": [],
            "tags": [],
            "shodan_accessible": False
        }

        # 1. Resolve IPs
        try:
            addr_info = socket.getaddrinfo(domain, 80, socket.AF_INET, socket.SOCK_STREAM)
            ips = list(set([item[4][0] for item in addr_info]))
            result["ip_addresses"] = ips
        except Exception:
            try:
                ip = socket.gethostbyname(domain)
                result["ip_addresses"] = [ip]
            except Exception:
                return result

        # 2. Reverse DNS
        for ip in result["ip_addresses"]:
            try:
                rev = socket.gethostbyaddr(ip)[0]
                result["reverse_dns"].append(rev)
            except Exception:
                pass

        # 3. Query Shodan InternetDB (Free, keyless, open endpoint)
        if result["ip_addresses"]:
            primary_ip = result["ip_addresses"][0]
            try:
                url = f"https://internetdb.shodan.io/{primary_ip}"
                with httpx.Client(timeout=self.timeout) as client:
                    resp = client.get(url)
                    if resp.status_code == 200:
                        data = resp.json()
                        result["shodan_accessible"] = True
                        result["open_ports"] = data.get("ports", [])
                        result["cpes"] = data.get("cpes", [])
                        result["vulns"] = data.get("vulns", [])
                        result["hostnames"] = data.get("hostnames", [])
                        result["tags"] = data.get("tags", [])
            except Exception:
                pass

        # 4. Fallback lightweight local port probe if InternetDB had no record
        if not result["open_ports"]:
            common_ports = [80, 443, 8080, 8443, 22]
            for p in common_ports:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.8)
                    if s.connect_ex((domain, p)) == 0:
                        result["open_ports"].append(p)
                    s.close()
                except Exception:
                    pass

        return result
