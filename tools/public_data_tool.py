"""
Layer 9: GitHub Org API & Public Data Scanner Tool
Paginates the public GitHub organization repositories API to return accurate total counts
and language distribution. Respects unauthenticated rate limits with clear User-Agent.
"""
import httpx
import time
from typing import Dict, Any
from collections import Counter

class ZeroCostPublicDataTool:
    def __init__(self, timeout: float = 6.0):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "ProspectIntelligenceOS/1.0 (research; +https://github.com/prospect-intelligence-os)",
            "Accept": "application/vnd.github+json"
        }

    def fetch_github_org_data(self, org_name: str) -> Dict[str, Any]:
        result = {"org_name": org_name, "public_repos": 0, "top_languages": []}

        try:
            # Step 1: Fetch org metadata for the authoritative public_repos count
            with httpx.Client(timeout=self.timeout, headers=self.headers) as client:
                org_resp = client.get(f"https://api.github.com/orgs/{org_name}")
                if org_resp.status_code != 200:
                    return result

                org_data = org_resp.json()
                result["public_repos"] = org_data.get("public_repos", 0)

                # Step 2: Paginate repos to build accurate language distribution
                # Cap at 5 pages (500 repos) to stay well within unauthenticated limits
                all_langs = []
                page = 1
                max_pages = 5

                while page <= max_pages:
                    repos_resp = client.get(
                        f"https://api.github.com/orgs/{org_name}/repos",
                        params={"per_page": 100, "page": page, "sort": "pushed"}
                    )
                    if repos_resp.status_code != 200:
                        break

                    repos = repos_resp.json()
                    if not repos:
                        break

                    all_langs.extend(r.get("language") for r in repos if r.get("language"))
                    page += 1

                    # Polite delay between pages to respect rate limits
                    if page <= max_pages:
                        time.sleep(0.25)

                result["top_languages"] = [lang for lang, _ in Counter(all_langs).most_common(5)]

        except Exception:
            pass

        return result
