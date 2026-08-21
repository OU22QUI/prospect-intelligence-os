"""
Layer 1: Identity, WHOIS & RDAP Scanner
Queries authoritative WHOIS and RDAP endpoints to discover domain registration dates,
registrar details, nameserver topology, and domain age.
"""
import socket
import re
import httpx
from typing import Dict, Any

class WhoisRdapScanner:
    def __init__(self, timeout: float = 4.0):
        self.timeout = timeout

    def scan(self, domain: str) -> Dict[str, Any]:
        domain = domain.strip().lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        result = {
            "domain": domain,
            "registrar": "Unknown",
            "creation_date": "Unknown",
            "name_servers": [],
            "registrant_org": "Privacy Protected",
            "query_source": "None"
        }

        # Try RDAP first (modern REST standard)
        try:
            rdap_url = f"https://rdap.org/domain/{domain}"
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                resp = client.get(rdap_url)
                if resp.status_code == 200:
                    data = resp.json()
                    result["query_source"] = "RDAP"
                    
                    # Events (creation date)
                    for event in data.get("events", []):
                        if event.get("eventAction") == "registration":
                            result["creation_date"] = event.get("eventDate", "")[:10]
                            break
                            
                    # Nameservers
                    ns_list = [ns.get("ldhName", "").lower() for ns in data.get("nameservers", []) if ns.get("ldhName")]
                    if ns_list:
                        result["name_servers"] = ns_list[:4]
                        
                    # Entities / Registrar
                    for entity in data.get("entities", []):
                        roles = entity.get("roles", [])
                        if "registrar" in roles:
                            vcard = entity.get("vcardArray", [])
                            if len(vcard) > 1:
                                for item in vcard[1]:
                                    if item[0] == "fn":
                                        result["registrar"] = item[3]
                                        break
                    if result["registrar"] != "Unknown" or result["creation_date"] != "Unknown":
                        return result
        except Exception:
            pass

        # Fallback to direct WHOIS socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect(("whois.iana.org", 43))
            s.send(f"{domain}\r\n".encode())

            whois_resp = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                whois_resp += data
            s.close()
            text = whois_resp.decode('utf-8', errors='ignore')

            whois_server_match = re.search(r"whois:\s*(\S+)", text, re.IGNORECASE)
            whois_server = whois_server_match.group(1) if whois_server_match else "whois.verisign-grs.com"

            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.settimeout(self.timeout)
            s2.connect((whois_server, 43))
            s2.send(f"{domain}\r\n".encode())

            tld_resp = b""
            while True:
                data = s2.recv(4096)
                if not data:
                    break
                tld_resp += data
            s2.close()
            tld_text = tld_resp.decode('utf-8', errors='ignore')

            result["query_source"] = "WHOIS_Socket"

            reg_match = re.search(r"Registrar:\s*(.+)", tld_text, re.IGNORECASE)
            if reg_match:
                result["registrar"] = reg_match.group(1).strip()

            created_match = re.search(r"(Creation Date|Created|registered):\s*(.+)", tld_text, re.IGNORECASE)
            if created_match:
                result["creation_date"] = created_match.group(2).strip()[:10]

            ns_matches = re.findall(r"Name Server:\s*(\S+)", tld_text, re.IGNORECASE)
            if ns_matches:
                result["name_servers"] = list(set([ns.lower() for ns in ns_matches[:4]]))

            org_match = re.search(r"Registrant Organization:\s*(.+)", tld_text, re.IGNORECASE)
            if org_match:
                result["registrant_org"] = org_match.group(1).strip()

        except Exception:
            pass

        return result
