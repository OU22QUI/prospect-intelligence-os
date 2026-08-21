"""
Ad Pixels & Growth Marketing Stack Detector
"""
import httpx
from typing import Dict, Any

class ZeroCostAdPixelsTool:
    def __init__(self, timeout: float = 4.0):
        self.timeout = timeout
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    def detect_pixels(self, domain: str) -> Dict[str, Any]:
        domain = domain.strip().lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        url = f"https://{domain}"

        result = {
            "runs_paid_ads": False,
            "detected_pixels": [],
            "marketing_stack": [],
            "tag_manager_present": False
        }

        try:
            with httpx.Client(timeout=self.timeout, headers=self.headers, follow_redirects=True) as client:
                resp = client.get(url)
                html = resp.text.lower()

                if "connect.facebook.net" in html or "fbq(" in html:
                    result["detected_pixels"].append("Meta (Facebook) Pixel")
                    result["runs_paid_ads"] = True

                if "googleadservices.com" in html or "gtag('config', 'aw-" in html or "google_conversion" in html:
                    result["detected_pixels"].append("Google Ads Pixel")
                    result["runs_paid_ads"] = True

                if "snap.licdn.com" in html or "linkedin_partner_id" in html or "_linkedin_data_partner_ids" in html:
                    result["detected_pixels"].append("LinkedIn Insight Tag")
                    result["runs_paid_ads"] = True

                if "analytics.tiktok.com" in html or "ttq.load" in html:
                    result["detected_pixels"].append("TikTok Pixel")
                    result["runs_paid_ads"] = True

                if "googletagmanager.com/gtm.js" in html or "gtm-" in html:
                    result["tag_manager_present"] = True
                    result["marketing_stack"].append("Google Tag Manager")

                if "static.klaviyo.com" in html or "_learnq" in html:
                    result["marketing_stack"].append("Klaviyo")

                if "js.hs-scripts.com" in html or "hubspot" in html:
                    result["marketing_stack"].append("HubSpot Marketing")

                if "static.hotjar.com" in html or "hj(" in html:
                    result["marketing_stack"].append("Hotjar Heatmaps")

                if "cdn.segment.com" in html or "analytics.page" in html:
                    result["marketing_stack"].append("Segment CDP")

        except Exception:
            pass

        return result
