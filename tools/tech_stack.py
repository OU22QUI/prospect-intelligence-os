"""
Layer 6: Technology Stack & Framework Scanner
Analyzes HTML, DOM signatures, meta tags, and script sources to detect frontend/backend frameworks,
CMS platforms, e-commerce engines, and libraries.

Uses high-precision structural signals (script src paths, meta generator tags, DOM element IDs,
specific CDN hostnames) over loose keyword matching to minimize false positives.
"""
import httpx
from bs4 import BeautifulSoup
import re
from typing import Dict, Any, List

class TechStackScanner:
    def __init__(self, timeout: float = 4.0):
        self.timeout = timeout
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    def _script_srcs(self, soup: BeautifulSoup) -> List[str]:
        """Extract all script src attributes as lowercase strings."""
        return [
            (tag.get("src") or "").lower()
            for tag in soup.find_all("script", src=True)
        ]

    def _link_hrefs(self, soup: BeautifulSoup) -> List[str]:
        """Extract all link href attributes as lowercase strings."""
        return [
            (tag.get("href") or "").lower()
            for tag in soup.find_all("link", href=True)
        ]

    def scan(self, domain: str) -> Dict[str, Any]:
        domain = domain.strip().lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        url = f"https://{domain}"

        result = {
            "domain": domain,
            "cms": "Custom / Headless",
            "frontend_frameworks": [],
            "ui_libraries": [],
            "backend_signals": [],
            "ecommerce": None
        }

        try:
            with httpx.Client(timeout=self.timeout, headers=self.headers, follow_redirects=True) as client:
                resp = client.get(url)
                if resp.status_code != 200:
                    return result
                
                html = resp.text
                html_lower = html.lower()
                soup = BeautifulSoup(html, "html.parser")

                script_srcs = self._script_srcs(soup)
                link_hrefs = self._link_hrefs(soup)

                # =================================================================
                # CMS Detection — structural signals only
                # =================================================================

                # WordPress: /wp-content/ or /wp-includes/ paths in scripts/links
                if any("/wp-content/" in s or "/wp-includes/" in s for s in script_srcs + link_hrefs):
                    result["cms"] = "WordPress"

                # Webflow: meta generator or webflow.js script
                elif self._has_meta_generator(soup, "webflow") or \
                     any("webflow" in s and s.endswith(".js") for s in script_srcs):
                    result["cms"] = "Webflow"

                # Shopify: cdn.shopify.com in script/link sources (structural, not body text)
                elif any("cdn.shopify.com" in s for s in script_srcs + link_hrefs):
                    result["cms"] = "Shopify"
                    result["ecommerce"] = "Shopify"

                # Framer: framer.com or framerusercontent.com in script/link sources
                elif any("framer.com" in s or "framerusercontent.com" in s for s in script_srcs + link_hrefs):
                    result["cms"] = "Framer"

                # Ghost: meta generator or ghost-specific script paths
                elif self._has_meta_generator(soup, "ghost"):
                    result["cms"] = "Ghost"

                # Wix: parastorage.com or wix-code-sdk in script sources
                elif any("parastorage.com" in s or "wix-code-sdk" in s for s in script_srcs):
                    result["cms"] = "Wix"

                # Squarespace: squarespace-cdn or meta generator
                elif any("squarespace-cdn" in s or "squarespace.com" in s for s in script_srcs + link_hrefs) or \
                     self._has_meta_generator(soup, "squarespace"):
                    result["cms"] = "Squarespace"

                # HubSpot CMS: hs-scripts.com or hubspot.net in script sources
                elif any("hs-scripts.com" in s or "js.hubspot.net" in s for s in script_srcs):
                    result["cms"] = "HubSpot CMS"

                # =================================================================
                # Frontend Frameworks — DOM element IDs and specific script paths
                # =================================================================

                # Next.js: __next div ID or /_next/ static asset paths
                if soup.find(id="__next") or any("/_next/" in s for s in script_srcs + link_hrefs):
                    result["frontend_frameworks"].append("Next.js / React")
                # React (standalone): react-dom or react.production script bundles
                elif any(re.search(r'react[-.]dom|react\.production', s) for s in script_srcs):
                    result["frontend_frameworks"].append("React")

                # Nuxt.js: __nuxt div ID or /_nuxt/ asset paths
                if soup.find(id="__nuxt") or any("/_nuxt/" in s for s in script_srcs + link_hrefs):
                    result["frontend_frameworks"].append("Nuxt.js / Vue")
                # Vue (standalone): vue.js or vue.global script paths
                elif any(re.search(r'vue[\.\-]', s) and (".js" in s) for s in script_srcs):
                    result["frontend_frameworks"].append("Vue.js")

                # Svelte / SvelteKit: .svelte-kit paths or svelte-specific attributes
                if any("svelte" in s and ".js" in s for s in script_srcs) or \
                   any(".svelte-kit" in s for s in script_srcs + link_hrefs):
                    result["frontend_frameworks"].append("Svelte")

                # Angular: ng-version attribute on root element or angular.js/zone.js scripts
                root_el = soup.find(attrs={"ng-version": True})
                if root_el or any(re.search(r'angular[\.\-]|zone\.js', s) for s in script_srcs):
                    result["frontend_frameworks"].append("Angular")

                # =================================================================
                # UI Libraries — CDN paths and specific class patterns
                # =================================================================
                if any("tailwindcss" in s or "tailwind" in s for s in link_hrefs + script_srcs):
                    result["ui_libraries"].append("Tailwind CSS")

                if any(re.search(r'bootstrap[\.\-]', s) for s in link_hrefs + script_srcs):
                    result["ui_libraries"].append("Bootstrap")

                # =================================================================
                # E-Commerce — structural asset paths
                # =================================================================
                if any("woocommerce" in s for s in script_srcs + link_hrefs):
                    result["ecommerce"] = "WooCommerce"
                elif any("magento" in s for s in script_srcs + link_hrefs):
                    result["ecommerce"] = "Magento"
                elif any("bigcommerce" in s for s in script_srcs + link_hrefs):
                    result["ecommerce"] = "BigCommerce"

                # =================================================================
                # Backend / Generator signals from meta tag
                # =================================================================
                gen = soup.find("meta", attrs={"name": "generator"})
                if gen and gen.get("content"):
                    result["backend_signals"].append(f"Generator: {gen.get('content')}")

                result["frontend_frameworks"] = list(dict.fromkeys(result["frontend_frameworks"]))
                result["ui_libraries"] = list(dict.fromkeys(result["ui_libraries"]))

        except Exception:
            pass

        return result

    @staticmethod
    def _has_meta_generator(soup: BeautifulSoup, keyword: str) -> bool:
        """Check if the meta generator tag contains a specific keyword."""
        gen = soup.find("meta", attrs={"name": "generator"})
        if gen and gen.get("content"):
            return keyword.lower() in gen["content"].lower()
        return False
