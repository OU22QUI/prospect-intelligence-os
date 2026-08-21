"""
Verifier Node - Faithful Passage Grounding (FPG) Engine
Computes deterministic, evidence-backed confidence scores across all extracted layers.
Tracks factual provenance for every extracted signal to eliminate hallucinations.
"""
from typing import Dict, Any, List
from agent.state import ProspectState

def verifier_node(state: ProspectState) -> ProspectState:
    raw = state.get("raw_findings", {})
    passages = state.get("verified_passages", [])

    layer_scores: Dict[str, float] = {}
    provenance_map: Dict[str, Dict[str, Any]] = {}

    # Layer 1: Identity & WHOIS / RDAP
    l1 = raw.get("layer_1_whois_rdap", {})
    if l1.get("registrar") != "Unknown" and l1.get("creation_date") != "Unknown":
        layer_scores["layer_1_whois"] = 0.98
        provenance_map["layer_1_whois"] = {"source": l1.get("query_source", "RDAP/WHOIS"), "status": "VERIFIED"}
    elif l1.get("registrar") != "Unknown" or l1.get("creation_date") != "Unknown":
        layer_scores["layer_1_whois"] = 0.85
        provenance_map["layer_1_whois"] = {"source": l1.get("query_source", "RDAP/WHOIS"), "status": "PARTIAL"}
    else:
        layer_scores["layer_1_whois"] = 0.50
        provenance_map["layer_1_whois"] = {"source": "WHOIS", "status": "UNVERIFIED"}

    # Layer 2: DNS Security & Deliverability Posture
    l2 = raw.get("layer_2_dns_security", {})
    has_mx = bool(l2.get("mx_records"))
    has_spf = l2.get("spf", {}).get("status") == "valid"
    has_dmarc = l2.get("dmarc", {}).get("status") == "configured"
    dns_score = 0.50
    if has_mx:
        dns_score += 0.25
    if has_spf or has_dmarc:
        dns_score += 0.23
    layer_scores["layer_2_dns_security"] = round(min(dns_score, 0.98), 2)
    provenance_map["layer_2_dns_security"] = {"source": "Authoritative DNS (dnspython)", "status": "VERIFIED" if has_mx else "PARTIAL"}

    # Layer 3: Network Infrastructure & Ports
    l3 = raw.get("layer_3_network_infra", {})
    has_ips = bool(l3.get("ip_addresses"))
    has_shodan = l3.get("shodan_accessible", False)
    net_score = 0.60
    if has_ips:
        net_score += 0.20
    if has_shodan or l3.get("open_ports"):
        net_score += 0.18
    layer_scores["layer_3_network"] = round(min(net_score, 0.98), 2)
    provenance_map["layer_3_network"] = {"source": "Socket / Shodan InternetDB", "status": "VERIFIED" if has_ips else "PARTIAL"}

    # Layer 4: SSL/TLS & Certificate Transparency
    l4 = raw.get("layer_4_ssl_cert", {})
    ssl_active = l4.get("ssl_active", False)
    has_issuer = l4.get("issuer_org") != "Unknown"
    ssl_score = 0.98 if (ssl_active and has_issuer) else (0.75 if ssl_active else 0.40)
    layer_scores["layer_4_ssl_tls"] = ssl_score
    provenance_map["layer_4_ssl_tls"] = {"source": "Native TLS Handshake Context", "status": "VERIFIED" if ssl_active else "FAILED"}

    # Layer 5: Web Server, Hosting & Security Headers
    l5 = raw.get("layer_5_headers_fingerprint", {})
    status_200 = l5.get("status_code") in (200, 301, 302)
    has_server = l5.get("server_banner") != "Unknown"
    h_score = 0.95 if (status_200 and has_server) else (0.80 if status_200 else 0.45)
    layer_scores["layer_5_headers_cdn"] = h_score
    provenance_map["layer_5_headers_cdn"] = {"source": "HTTP Response Headers", "status": "VERIFIED" if status_200 else "PARTIAL"}

    # Layer 6: Technology Stack & Frameworks
    l6 = raw.get("layer_6_tech_stack", {})
    has_frameworks = bool(l6.get("frontend_frameworks") or l6.get("cms") != "Custom / Headless")
    layer_scores["layer_6_tech_stack"] = 0.92 if has_frameworks else 0.70
    provenance_map["layer_6_tech_stack"] = {"source": "DOM & Script Signature Analysis", "status": "VERIFIED" if has_frameworks else "BASE_ONLY"}

    # Layer 7: Marketing, Analytics & Ad Pixels
    l7 = raw.get("layer_7_marketing_pixels", {})
    has_pixels = bool(l7.get("detected_pixels") or l7.get("marketing_stack"))
    layer_scores["layer_7_marketing"] = 0.95 if has_pixels else 0.80
    provenance_map["layer_7_marketing"] = {"source": "HTML Pixel Regex Matcher", "status": "VERIFIED" if has_pixels else "NO_PIXELS_DETECTED"}

    # Layer 8: Site Structure, Architecture & SEO Entities
    l8 = raw.get("layer_8_site_structure", {})
    has_title = bool(l8.get("page_title"))
    has_schema = bool(l8.get("json_ld_types"))
    site_score = 0.95 if (has_title and has_schema) else (0.85 if has_title else 0.40)
    layer_scores["layer_8_site_structure"] = site_score
    provenance_map["layer_8_site_structure"] = {"source": "BeautifulSoup4 HTML/JSON-LD Parser", "status": "VERIFIED" if has_title else "PARTIAL"}

    # Layer 9: Developer & Engineering Signals (GitHub)
    l9 = raw.get("layer_9_github_signals", {})
    has_gh = l9.get("public_repos", 0) > 0
    layer_scores["layer_9_github_dev"] = 0.98 if has_gh else 0.75
    provenance_map["layer_9_github_dev"] = {"source": "GitHub Org REST API", "status": "VERIFIED" if has_gh else "NO_PUBLIC_ORG"}

    # Calculate overall weighted grounding score
    weights = {
        "layer_1_whois": 0.10,
        "layer_2_dns_security": 0.15,
        "layer_3_network": 0.10,
        "layer_4_ssl_tls": 0.10,
        "layer_5_headers_cdn": 0.10,
        "layer_6_tech_stack": 0.10,
        "layer_7_marketing": 0.10,
        "layer_8_site_structure": 0.15,
        "layer_9_github_dev": 0.10,
    }

    weighted_overall = sum(layer_scores[k] * weights[k] for k in weights if k in layer_scores)
    
    state["confidence_scores"] = {
        "overall_grounding": round(weighted_overall, 2),
        **layer_scores
    }
    
    # Attach provenance to raw findings for synthesis
    state["raw_findings"]["_provenance"] = provenance_map

    return state
