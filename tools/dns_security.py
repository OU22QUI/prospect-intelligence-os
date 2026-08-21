"""
Layer 2: DNS Security & Deliverability Posture Scanner
Audits SPF, DMARC policies, DKIM selector existence, CAA records, and IPv6 readiness.
"""
import dns.resolver
import re
from typing import Dict, Any

class DnsSecurityScanner:
    def __init__(self, timeout: float = 3.0):
        self.timeout = timeout

    def scan(self, domain: str) -> Dict[str, Any]:
        domain = domain.strip().lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        
        report = {
            "domain": domain,
            "mx_records": [],
            "email_provider": "Unknown",
            "spf": {"status": "missing", "record": "", "lookup_count": 0, "has_all_qualifier": False},
            "dmarc": {"status": "missing", "policy": "none", "record": ""},
            "dkim_selectors_found": [],
            "has_ipv6": False,
            "caa_records": []
        }

        # 1. MX Records & Provider Fingerprinting
        try:
            mx_records = dns.resolver.resolve(domain, 'MX', lifetime=self.timeout)
            mx_list = [str(r.exchange).rstrip('.').lower() for r in mx_records]
            report["mx_records"] = mx_list
            
            mx_str = " ".join(mx_list)
            if "google" in mx_str or "l.google.com" in mx_str:
                report["email_provider"] = "Google Workspace"
            elif "outlook.com" in mx_str or "protection.outlook.com" in mx_str:
                report["email_provider"] = "Microsoft 365"
            elif "mimecast" in mx_str:
                report["email_provider"] = "Mimecast"
            elif "pphosted" in mx_str or "proofpoint" in mx_str:
                report["email_provider"] = "Proofpoint"
            elif mx_list:
                report["email_provider"] = "Custom / Self-Hosted Mail Server"
        except Exception:
            pass

        # 2. SPF Audit
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT', lifetime=self.timeout)
            for rdata in txt_records:
                txt_str = "".join([b.decode('utf-8', errors='ignore') for b in rdata.strings])
                if txt_str.startswith("v=spf1"):
                    report["spf"]["status"] = "valid"
                    report["spf"]["record"] = txt_str
                    includes = re.findall(r"include:(\S+)", txt_str)
                    report["spf"]["lookup_count"] = len(includes)
                    if "~all" in txt_str or "-all" in txt_str:
                        report["spf"]["has_all_qualifier"] = True
                    break
        except Exception:
            pass

        # 3. DMARC Audit (_dmarc.domain)
        try:
            dmarc_txt = dns.resolver.resolve(f"_dmarc.{domain}", 'TXT', lifetime=self.timeout)
            for rdata in dmarc_txt:
                txt_str = "".join([b.decode('utf-8', errors='ignore') for b in rdata.strings])
                if "v=DMARC1" in txt_str:
                    report["dmarc"]["status"] = "configured"
                    report["dmarc"]["record"] = txt_str
                    p_match = re.search(r"p=(reject|quarantine|none)", txt_str, re.IGNORECASE)
                    if p_match:
                        report["dmarc"]["policy"] = p_match.group(1).lower()
                    break
        except Exception:
            pass

        # 4. Common DKIM Selectors
        selectors = ["google", "default", "k1", "selector1", "s1", "mail", "dkim", "mandrill", "smtp"]
        for sel in selectors:
            try:
                dns.resolver.resolve(f"{sel}._domainkey.{domain}", 'TXT', lifetime=1.2)
                report["dkim_selectors_found"].append(sel)
            except Exception:
                try:
                    dns.resolver.resolve(f"{sel}._domainkey.{domain}", 'CNAME', lifetime=1.2)
                    report["dkim_selectors_found"].append(sel)
                except Exception:
                    pass

        # 5. IPv6 (AAAA)
        try:
            aaaa = dns.resolver.resolve(domain, 'AAAA', lifetime=self.timeout)
            if len(aaaa) > 0:
                report["has_ipv6"] = True
        except Exception:
            pass

        # 6. CAA Records
        try:
            caa = dns.resolver.resolve(domain, 'CAA', lifetime=self.timeout)
            report["caa_records"] = [str(r) for r in caa]
        except Exception:
            pass

        return report
