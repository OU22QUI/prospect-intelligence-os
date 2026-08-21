"""
Layer 5: Web Server, Hosting & Security Headers Fingerprinter
Audits HTTP response headers, Server banners, CDN presence (Cloudflare/Vercel/Fastly),
and calculates a defensive Security Headers Posture Score (HSTS, CSP, X-Frame, Referrer-Policy).
"""
import httpx
from typing import Dict, Any, List

class HeadersFingerprintScanner:
    def __init__(self, timeout: float = 4.0):
        self.timeout = timeout
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    def scan(self, domain: str) -> Dict[str, Any]:
        domain = domain.strip().lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        url = f"https://{domain}"

        result = {
            "domain": domain,
            "status_code": 0,
            "server_banner": "Unknown",
            "detected_cdn": [],
            "hosting_platform": "Unknown",
            "framework_header": None,
            "security_headers": {
                "strict_transport_security": False,
                "content_security_policy": False,
                "x_frame_options": False,
                "x_content_type_options": False,
                "referrer_policy": False,
                "permissions_policy": False
            },
            "security_posture_score": 0,
            "raw_interesting_headers": {}
        }

        try:
            with httpx.Client(timeout=self.timeout, headers=self.headers, follow_redirects=True) as client:
                resp = client.get(url)
                result["status_code"] = resp.status_code
                headers = {k.lower(): v for k, v in resp.headers.items()}

                # Server Banner
                if "server" in headers:
                    result["server_banner"] = headers["server"]

                # CDN & Hosting Detection
                server_lower = headers.get("server", "").lower()
                if "cloudflare" in server_lower or "cf-ray" in headers:
                    result["detected_cdn"].append("Cloudflare")
                if "akamai" in server_lower or "x-akamai" in headers:
                    result["detected_cdn"].append("Akamai")
                if "fastly" in server_lower or "x-fastly" in headers:
                    result["detected_cdn"].append("Fastly")
                if "cloudfront" in server_lower or "x-amz-cf-id" in headers:
                    result["detected_cdn"].append("AWS CloudFront")

                if "x-vercel-id" in headers:
                    result["hosting_platform"] = "Vercel"
                elif "x-render-origin-server" in headers:
                    result["hosting_platform"] = "Render"
                elif "fly-request-id" in headers:
                    result["hosting_platform"] = "Fly.io"
                elif "x-powered-by" in headers:
                    result["framework_header"] = headers["x-powered-by"]

                # Security Headers Evaluation
                sec = result["security_headers"]
                if "strict-transport-security" in headers:
                    sec["strict_transport_security"] = True
                if "content-security-policy" in headers:
                    sec["content_security_policy"] = True
                if "x-frame-options" in headers:
                    sec["x_frame_options"] = True
                if "x-content-type-options" in headers:
                    sec["x_content_type_options"] = True
                if "referrer-policy" in headers:
                    sec["referrer_policy"] = True
                if "permissions-policy" in headers:
                    sec["permissions_policy"] = True

                score = int((sum(1 for v in sec.values() if v) / len(sec)) * 100)
                result["security_posture_score"] = score

                # Select interesting headers
                for k in ["server", "x-powered-by", "cf-ray", "x-vercel-id", "x-nextjs-page"]:
                    if k in headers:
                        result["raw_interesting_headers"][k] = headers[k]

        except Exception:
            pass

        return result
