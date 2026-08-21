"""
Layer 4: SSL/TLS & Certificate Transparency Scanner
Analyzes SSL/TLS peer certificate parameters, issuer, SAN extensions, and TLS protocol version.
"""
import socket
import ssl
from typing import Dict, Any, List

class SslCertificateScanner:
    def __init__(self, timeout: float = 3.5):
        self.timeout = timeout

    def scan(self, domain: str) -> Dict[str, Any]:
        domain = domain.strip().lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        
        result = {
            "domain": domain,
            "ssl_active": False,
            "tls_version": "Unknown",
            "cipher_suite": "Unknown",
            "issuer_org": "Unknown",
            "issuer_common_name": "Unknown",
            "valid_from": "Unknown",
            "valid_until": "Unknown",
            "subject_alt_names": []
        }

        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    result["ssl_active"] = True
                    result["tls_version"] = ssock.version()
                    result["cipher_suite"] = ssock.cipher()[0] if ssock.cipher() else "Unknown"

                    # Issuer
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    result["issuer_org"] = issuer.get('organizationName', 'Unknown')
                    result["issuer_common_name"] = issuer.get('commonName', 'Unknown')

                    # Validity
                    result["valid_from"] = cert.get('notBefore', 'Unknown')
                    result["valid_until"] = cert.get('notAfter', 'Unknown')

                    # Subject Alternative Names (SANs)
                    sans = [item[1] for item in cert.get('subjectAltName', []) if item[0] == 'DNS']
                    result["subject_alt_names"] = sans[:6]
        except Exception:
            pass

        return result
