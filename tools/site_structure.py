"""
Layer 8: Site Structure, Architecture & SEO Entity Scanner
Extracts page metadata, OpenGraph tags, JSON-LD Schema.org graphs, heading structures,
and tests for robots.txt / sitemap.xml presence.
"""
import httpx
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, Any, List

class SiteStructureScanner:
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    def scan(self, domain: str) -> Dict[str, Any]:
        domain = domain.strip().lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        url = f"https://{domain}"

        result = {
            "domain": domain,
            "page_title": "",
            "meta_description": "",
            "og_title": "",
            "og_description": "",
            "og_image": None,
            "json_ld_types": [],
            "core_headings": [],
            "has_robots_txt": False,
            "has_sitemap_xml": False,
            "canonical_url": None
        }

        try:
            with httpx.Client(timeout=self.timeout, headers=self.headers, follow_redirects=True) as client:
                resp = client.get(url)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")

                    if soup.title:
                        result["page_title"] = soup.title.get_text(strip=True)

                    desc = soup.find("meta", attrs={"name": "description"})
                    if desc:
                        result["meta_description"] = desc.get("content", "").strip()

                    og_t = soup.find("meta", property="og:title")
                    if og_t:
                        result["og_title"] = og_t.get("content", "").strip()

                    og_d = soup.find("meta", property="og:description")
                    if og_d:
                        result["og_description"] = og_d.get("content", "").strip()

                    og_img = soup.find("meta", property="og:image")
                    if og_img:
                        result["og_image"] = og_img.get("content", "").strip()

                    canon = soup.find("link", rel="canonical")
                    if canon:
                        result["canonical_url"] = canon.get("href", "").strip()

                    # JSON-LD Schema types
                    for script in soup.find_all("script", type="application/ld+json"):
                        try:
                            data = json.loads(script.string)
                            if isinstance(data, dict):
                                if "@type" in data:
                                    t = data["@type"]
                                    if isinstance(t, list):
                                        result["json_ld_types"].extend(t)
                                    else:
                                        result["json_ld_types"].append(t)
                            elif isinstance(data, list):
                                for item in data:
                                    if isinstance(item, dict) and "@type" in item:
                                        result["json_ld_types"].append(item["@type"])
                        except Exception:
                            pass

                    # Headings
                    headings = []
                    for h in soup.find_all(["h1", "h2"])[:6]:
                        txt = h.get_text(strip=True)
                        if 10 < len(txt) < 140:
                            headings.append(txt)
                    result["core_headings"] = headings

                # Robots.txt probe
                try:
                    r_resp = client.get(f"https://{domain}/robots.txt")
                    if r_resp.status_code == 200 and "user-agent" in r_resp.text.lower():
                        result["has_robots_txt"] = True
                except Exception:
                    pass

                # Sitemap probe
                try:
                    s_resp = client.get(f"https://{domain}/sitemap.xml")
                    if s_resp.status_code == 200 and ("<urlset" in s_resp.text.lower() or "<sitemapindex" in s_resp.text.lower()):
                        result["has_sitemap_xml"] = True
                except Exception:
                    pass

        except Exception:
            pass

        result["json_ld_types"] = list(set(result["json_ld_types"]))
        return result
