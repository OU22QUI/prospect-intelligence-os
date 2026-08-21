"""
Layer 10: Signal-Grounded Outreach Angle Generator (Insight-First & Non-Generic)
Synthesizes 3 distinct, highly contextualized, non-pitchy outreach angles derived strictly
from verified technical, deliverability, growth, and engineering parameters.
"""
from typing import Dict, Any, List

class SignalGroundedAngleGenerator:
    def generate_angles(self, dossier: Dict[str, Any]) -> List[Dict[str, Any]]:
        domain = dossier.get("domain", "")
        company_name = dossier.get("company_name") or domain.split(".")[0].capitalize()
        
        angles = []

        dns_sec = dossier.get("layer_2_dns_security", {})
        net_infra = dossier.get("layer_3_network_infra", {})
        ssl_data = dossier.get("layer_4_ssl_cert", {})
        headers_data = dossier.get("layer_5_headers_fingerprint", {})
        tech_data = dossier.get("layer_6_tech_stack", {})
        marketing_data = dossier.get("layer_7_marketing_pixels", {})
        site_data = dossier.get("layer_8_site_structure", {})
        github_data = dossier.get("layer_9_github_signals", {})
        whois_data = dossier.get("layer_1_whois_rdap", {})

        # =========================================================================
        # ANGLE 1: Deliverability Posture & Mail Infrastructure Optimization
        # =========================================================================
        dmarc_policy = dns_sec.get("dmarc", {}).get("policy", "none").lower()
        spf_status = dns_sec.get("spf", {}).get("status", "missing").lower()
        email_provider = dns_sec.get("email_provider", "Managed Mail Host")
        dkim_selectors = dns_sec.get("dkim_selectors_found", [])

        if dmarc_policy == "none":
            angle_1 = {
                "pillar": "Deliverability & Authentication Hardening",
                "factual_trigger": f"Domain {domain} publishes a DMARC p=none policy without active enforcement.",
                "angle_thesis": "Google and Yahoo inbox algorithms deprioritize or quarantine unaligned domain traffic lacking strict DMARC enforcement.",
                "sample_hook": f"Looking at domain deliverability for {company_name}—noticed the root domain is currently publishing a 'p=none' DMARC policy. Given strict receiver requirement updates from Google and Yahoo, are you seeing any impact on transactional or outbound placement?"
            }
        elif spf_status != "valid":
            angle_1 = {
                "pillar": "Deliverability & SPF Alignment",
                "factual_trigger": f"SPF record for {domain} is missing or has lookup syntax irregularities.",
                "angle_thesis": "Uncertified SPF lookup chains degrade receiver domain reputation scores during third-party mail routing.",
                "sample_hook": f"Checked {domain}'s DNS records and noticed the SPF string appears unaligned. Has your infrastructure team flagged any receiver lookup limit issues when routing outbound through third-party services?"
            }
        else:
            dkim_str = f" ({', '.join(dkim_selectors[:2])} selectors)" if dkim_selectors else ""
            angle_1 = {
                "pillar": "Infrastructure Integration & Mail Flow",
                "factual_trigger": f"Domain operates on {email_provider} with strict DMARC {dmarc_policy.upper()} policy{dkim_str}.",
                "angle_thesis": "Hardened mail security postures require zero-friction DKIM/SPF alignment when integrating external workflow automation.",
                "sample_hook": f"Noticed {company_name} maintains a hardened {email_provider} setup with strict DMARC {dmarc_policy.upper()} enforcement. When connecting external data or enrichment tooling into your workflow, how do you handle DKIM selector alignment without compromising sender reputation?"
            }
        angles.append(angle_1)

        # =========================================================================
        # ANGLE 2: Paid Acquisition Footprint & Growth Infrastructure
        # =========================================================================
        runs_ads = marketing_data.get("runs_paid_ads", False)
        detected_pixels = marketing_data.get("detected_pixels", [])
        mkt_stack = marketing_data.get("marketing_stack", [])
        analytics_summary = ", ".join(mkt_stack) if mkt_stack else ""

        if runs_ads and detected_pixels:
            pixels_str = ", ".join(detected_pixels[:2])
            angle_2 = {
                "pillar": "Paid Acquisition Synergy & Intent Filtering",
                "factual_trigger": f"Active ad tracking pixels detected: {pixels_str} (Stack: {analytics_summary or 'Standard Analytics'}).",
                "angle_thesis": "Heavy paid retargeting spend risks budget burn on low-intent clicks without real-time account-level technographic filtering.",
                "sample_hook": f"Saw {company_name} is running active paid retargeting ({pixels_str}). Are you using account-level technographic signals to filter out low-intent clicks before they hit your ad budget?"
            }
        elif mkt_stack:
            stack_str = ", ".join(mkt_stack[:2])
            angle_2 = {
                "pillar": "Analytics Stack & Data Pipeline Enrichment",
                "factual_trigger": f"Marketing and analytics event routing detected: {stack_str}.",
                "angle_thesis": "Modern customer data pipelines benefit from passing raw technographic signals directly into event streams rather than relying on static form fills.",
                "sample_hook": f"Noticed {company_name}'s web setup routes events through {stack_str}. Are you currently enriching incoming lead events with live technographic/DNS signals at the data layer, or relying mostly on form inputs?"
            }
        else:
            angle_2 = {
                "pillar": "Organic B2B Account Intelligence",
                "factual_trigger": f"Zero third-party ad tracking pixels or retargeting scripts detected on {domain}.",
                "angle_thesis": "Reliance on organic positioning means targeted direct account selection is the primary driver for high-value client acquisition.",
                "sample_hook": f"Checked {domain}'s front-end tracking—looks like {company_name} relies purely on organic positioning rather than heavy paid ad pixels. How is your team currently identifying in-market accounts before they land on your site?"
            }
        angles.append(angle_2)

        # =========================================================================
        # ANGLE 3: Engineering Velocity & Modern Architecture
        # =========================================================================
        public_repos = github_data.get("public_repos", 0)
        top_langs = github_data.get("top_languages", [])
        cms = tech_data.get("cms", "Custom / Headless")
        frontend = tech_data.get("frontend_frameworks", [])
        server_banner = headers_data.get("server_banner", "Standard Web Server")
        cdn = ", ".join(headers_data.get("detected_cdn", [])) or "Direct CDN"

        if public_repos > 0 and top_langs:
            langs_str = ", ".join(top_langs[:2])
            angle_3 = {
                "pillar": "Developer Velocity & Technical Stack",
                "factual_trigger": f"Active public GitHub organization with {public_repos} public repositories (primary languages: {langs_str}).",
                "angle_thesis": "High public engineering velocity indicates a developer-first culture that values structured JSON schemas and API-first tooling.",
                "sample_hook": f"Noticed {company_name}'s GitHub org has {public_repos} public repos with heavy {langs_str} activity. Is your engineering team maintaining custom internal scrapers for account intelligence, or leveraging structured schema-validated APIs?"
            }
        elif frontend or cms != "Custom / Headless":
            fe_str = ", ".join(frontend) if frontend else cms
            angle_3 = {
                "pillar": "Modern Web Architecture & Headless Integration",
                "factual_trigger": f"Web architecture running on {fe_str} deployed via {cdn}.",
                "angle_thesis": "Modern edge/SSR architectures require light-footprint API contracts when syncing external account metadata.",
                "sample_hook": f"Saw {company_name}'s web platform is built on {fe_str} deployed via {cdn}. When pulling company and technical metadata into your application, do you consume raw OSINT endpoints or rely on pre-parsed JSON schemas?"
            }
        else:
            page_title = site_data.get("page_title") or f"Positioning at {company_name}"
            clean_title = page_title.split("|")[0].split("-")[0].strip()
            angle_3 = {
                "pillar": "Strategic Technical Alignment",
                "factual_trigger": f"Published core product positioning: '{clean_title}'.",
                "angle_thesis": "Aligning technical research automation with published core product focus.",
                "sample_hook": f"Looking into {company_name}'s core positioning around '{clean_title}'—curious how your team currently evaluates technical fit when qualifying new target accounts."
            }
        angles.append(angle_3)

        return angles
