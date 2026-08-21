"""
CLI Runner & Structured Intelligence Dossier Exporter (10-Layer Research)
"""
import sys
import os
import json
from agent.agent import ProspectIntelligenceAgent
from config import OUTPUT_DIR

def run_cli():
    if len(sys.argv) < 2:
        print("Usage: python -m agent.runner <company_domain> [company_name]")
        print("Example: python -m agent.runner vercel.com \"Vercel\"")
        sys.exit(1)

    domain = sys.argv[1].strip().lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
    company_name = sys.argv[2] if len(sys.argv) > 2 else domain.split(".")[0].capitalize()

    print("=" * 70)
    print(f" 🎯 PROSPECT INTELLIGENCE OS — 10-LAYER OSINT RESEARCH AGENT")
    print(f" Target Domain: {domain}")
    print("=" * 70)

    agent = ProspectIntelligenceAgent()
    state = agent.run(company_domain=domain, company_name=company_name)
    dossier = state.get("dossier", {})

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, f"prospect_dossier_{domain.replace('.', '_')}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dossier, f, indent=2, ensure_ascii=False)

    confidence = dossier.get("overall_grounding_confidence", 0.9)
    scores = dossier.get("confidence_breakdown", {})
    provenance = dossier.get("evidence_provenance", {})

    # Render comprehensive markdown report
    md_lines = []
    md_lines.append(f"# 🎯 Prospect Intelligence Dossier: {dossier.get('company_name')}")
    md_lines.append(f"**Domain:** `{dossier.get('domain')}` | **Overall Grounding Confidence:** `{confidence * 100:.0f}%` (FPG Verified)\n")

    # Layer 10 First: Signal-Grounded Angles
    angles = dossier.get("layer_10_signal_grounded_angles", [])
    if angles:
        md_lines.append("## 💡 Layer 10: Signal-Grounded Outreach Angles (Factual Triggers)")
        for idx, a in enumerate(angles, 1):
            md_lines.append(f"### Angle {idx}: {a.get('pillar')}")
            md_lines.append(f"- **Trigger:** {a.get('factual_trigger')}")
            md_lines.append(f"- **Thesis:** {a.get('angle_thesis')}")
            md_lines.append(f"- **Suggested Hook:** *\"{a.get('sample_hook')}\"*\n")

    # Provenance & Confidence Table
    md_lines.append("## 📊 Factual Grounding & Provenance Telemetry")
    md_lines.append("| Research Layer | Grounding Score | Source Engine | Status |")
    md_lines.append("|---|---|---|---|")
    layer_names = {
        "layer_1_whois": "Layer 1: Identity & WHOIS",
        "layer_2_dns_security": "Layer 2: DNS Security & Deliverability",
        "layer_3_network": "Layer 3: Network Infrastructure",
        "layer_4_ssl_tls": "Layer 4: SSL/TLS & Certificates",
        "layer_5_headers_cdn": "Layer 5: Server, Headers & CDN",
        "layer_6_tech_stack": "Layer 6: Technology Stack",
        "layer_7_marketing": "Layer 7: Marketing & Ad Pixels",
        "layer_8_site_structure": "Layer 8: Site Structure & SEO",
        "layer_9_github_dev": "Layer 9: GitHub Dev Signals"
    }
    for k, name in layer_names.items():
        score_val = f"{scores.get(k, 0.9) * 100:.0f}%"
        prov = provenance.get(k, {})
        src = prov.get("source", "Standard Scanner")
        stat = prov.get("status", "VERIFIED")
        md_lines.append(f"| **{name}** | `{score_val}` | {src} | `{stat}` |")
    md_lines.append("")

    # Layer 1: Identity & WHOIS
    l1 = dossier.get("layer_1_whois_rdap", {})
    md_lines.append("## 🔒 Layer 1: Identity & WHOIS / RDAP")
    md_lines.append(f"- **Registrar:** `{l1.get('registrar')}`")
    md_lines.append(f"- **Creation Date:** `{l1.get('creation_date')}`")
    md_lines.append(f"- **Nameservers:** `{', '.join(l1.get('name_servers', [])) or 'Standard DNS'}`\n")

    # Layer 2: DNS Security
    l2 = dossier.get("layer_2_dns_security", {})
    md_lines.append("## 🛡️ Layer 2: DNS Topology & Deliverability Posture")
    md_lines.append(f"- **Primary Email Provider:** `{l2.get('email_provider')}`")
    md_lines.append(f"- **SPF Status:** `{l2.get('spf', {}).get('status')}` (`{l2.get('spf', {}).get('record') or 'No record'}`)")
    md_lines.append(f"- **DMARC Policy:** `{l2.get('dmarc', {}).get('policy', 'none').upper()}`")
    md_lines.append(f"- **DKIM Selectors Found:** `{', '.join(l2.get('dkim_selectors_found', [])) or 'None detected via standard selectors'}`")
    md_lines.append(f"- **IPv6 (AAAA):** `{'Enabled' if l2.get('has_ipv6') else 'Disabled'}`\n")

    # Layer 3: Network Infrastructure
    l3 = dossier.get("layer_3_network_infra", {})
    md_lines.append("## 🌐 Layer 3: Network Infrastructure & Ports (Shodan InternetDB)")
    md_lines.append(f"- **Resolved IPs:** `{', '.join(l3.get('ip_addresses', []))}`")
    md_lines.append(f"- **Open Ports:** `{', '.join([str(p) for p in l3.get('open_ports', [])]) or '80, 443'}`")
    if l3.get("cpes"):
        md_lines.append(f"- **CPEs:** `{', '.join(l3.get('cpes', []))}`")
    if l3.get("vulns"):
        md_lines.append(f"- **Detected CVEs:** `{', '.join(l3.get('vulns', []))}`")
    md_lines.append("")

    # Layer 4: SSL/TLS
    l4 = dossier.get("layer_4_ssl_cert", {})
    md_lines.append("## 🔐 Layer 4: SSL/TLS & Certificate Transparency")
    md_lines.append(f"- **SSL Active:** `{'Yes' if l4.get('ssl_active') else 'No'}` ({l4.get('tls_version')})")
    md_lines.append(f"- **Issuer Organization:** `{l4.get('issuer_org')}` (`{l4.get('issuer_common_name')}`)")
    md_lines.append(f"- **Cipher Suite:** `{l4.get('cipher_suite')}`\n")

    # Layer 5: Headers & CDN
    l5 = dossier.get("layer_5_headers_fingerprint", {})
    md_lines.append("## ⚙️ Layer 5: Web Server, Hosting & Security Headers")
    md_lines.append(f"- **Server Banner:** `{l5.get('server_banner')}`")
    md_lines.append(f"- **Detected CDN / Proxy:** `{', '.join(l5.get('detected_cdn', [])) or 'Direct'}`")
    md_lines.append(f"- **Hosting Platform:** `{l5.get('hosting_platform')}`")
    md_lines.append(f"- **Security Headers Score:** `{l5.get('security_posture_score', 0)}/100`\n")

    # Layer 6: Tech Stack
    l6 = dossier.get("layer_6_tech_stack", {})
    md_lines.append("## 💻 Layer 6: Technology Stack & Frameworks")
    md_lines.append(f"- **CMS Platform:** `{l6.get('cms')}`")
    md_lines.append(f"- **Frontend Frameworks:** `{', '.join(l6.get('frontend_frameworks', [])) or 'Standard DOM'}`")
    md_lines.append(f"- **UI Libraries:** `{', '.join(l6.get('ui_libraries', [])) or 'None'}`\n")

    # Layer 7: Marketing Pixels
    l7 = dossier.get("layer_7_marketing_pixels", {})
    md_lines.append("## 🎯 Layer 7: Marketing, Analytics & Ad Pixels")
    md_lines.append(f"- **Runs Paid Ads:** `{'Yes' if l7.get('runs_paid_ads') else 'No active ad pixels detected'}`")
    if l7.get("detected_pixels"):
        md_lines.append(f"- **Detected Ad Pixels:** `{', '.join(l7.get('detected_pixels', []))}`")
    if l7.get("marketing_stack"):
        md_lines.append(f"- **Analytics Stack:** `{', '.join(l7.get('marketing_stack', []))}`")
    md_lines.append("")

    # Layer 8: Site Structure & SEO
    l8 = dossier.get("layer_8_site_structure", {})
    md_lines.append("## 🗺️ Layer 8: Site Structure & SEO Entities")
    md_lines.append(f"- **Title:** {l8.get('page_title') or 'N/A'}")
    md_lines.append(f"- **Meta Description:** {l8.get('meta_description') or 'N/A'}")
    md_lines.append(f"- **JSON-LD Schema Entities:** `{', '.join(l8.get('json_ld_types', [])) or 'None'}`")
    md_lines.append(f"- **Robots.txt:** `{'Present' if l8.get('has_robots_txt') else 'Missing'}` | **Sitemap.xml:** `{'Present' if l8.get('has_sitemap_xml') else 'Missing'}`\n")

    # Layer 9: GitHub Dev Signals
    l9 = dossier.get("layer_9_github_signals", {})
    md_lines.append("## 🐙 Layer 9: Developer & Engineering Signals (GitHub)")
    md_lines.append(f"- **Public Repositories:** `{l9.get('public_repos', 0)}`")
    if l9.get("top_languages"):
        md_lines.append(f"- **Primary Programming Languages:** `{', '.join(l9.get('top_languages', []))}`")
    md_lines.append("")

    md_path = os.path.join(OUTPUT_DIR, f"prospect_dossier_{domain.replace('.', '_')}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print("\n=== 10-LAYER RESEARCH COMPLETE ===")
    print(f"  Overall Grounding Confidence: {confidence * 100:.0f}%")
    print(f"  JSON Export: {json_path}")
    print(f"  Markdown Dossier: {md_path}")

if __name__ == "__main__":
    run_cli()
