"""
Multi-Layer OSINT Research Execution Node (Layers 1-9)
Executes all 9 foundational signal scanners across DNS, network, TLS, HTTP, stack, marketing, and GitHub.
"""
from agent.state import ProspectState
from tools.whois_rdap import WhoisRdapScanner
from tools.dns_security import DnsSecurityScanner
from tools.network_infra import NetworkInfraScanner
from tools.ssl_cert_transparency import SslCertificateScanner
from tools.headers_fingerprint import HeadersFingerprintScanner
from tools.tech_stack import TechStackScanner
from tools.ad_pixels_tool import ZeroCostAdPixelsTool
from tools.site_structure import SiteStructureScanner
from tools.public_data_tool import ZeroCostPublicDataTool

def research_layers_node(state: ProspectState) -> ProspectState:
    domain = state["company_domain"]
    name = state["company_name"]

    # Layer 1: Identity & WHOIS
    whois_tool = WhoisRdapScanner()
    l1_data = whois_tool.scan(domain)

    # Layer 2: DNS Security & Deliverability
    dns_tool = DnsSecurityScanner()
    l2_data = dns_tool.scan(domain)

    # Layer 3: Network Infra & InternetDB
    net_tool = NetworkInfraScanner()
    l3_data = net_tool.scan(domain)

    # Layer 4: SSL/TLS & Cert Transparency
    ssl_tool = SslCertificateScanner()
    l4_data = ssl_tool.scan(domain)

    # Layer 5: Headers, Server & CDN
    headers_tool = HeadersFingerprintScanner()
    l5_data = headers_tool.scan(domain)

    # Layer 6: Tech Stack & Frameworks
    tech_tool = TechStackScanner()
    l6_data = tech_tool.scan(domain)

    # Layer 7: Marketing Pixels & Analytics
    pixels_tool = ZeroCostAdPixelsTool()
    l7_data = pixels_tool.detect_pixels(domain)

    # Layer 8: Site Structure & SEO Entities
    site_tool = SiteStructureScanner()
    l8_data = site_tool.scan(domain)

    # Layer 9: Public GitHub Signals
    gh_tool = ZeroCostPublicDataTool()
    clean_org = name.lower().replace(" ", "").replace("-", "")
    l9_data = gh_tool.fetch_github_org_data(clean_org)

    state["raw_findings"] = {
        "layer_1_whois_rdap": l1_data,
        "layer_2_dns_security": l2_data,
        "layer_3_network_infra": l3_data,
        "layer_4_ssl_cert": l4_data,
        "layer_5_headers_fingerprint": l5_data,
        "layer_6_tech_stack": l6_data,
        "layer_7_marketing_pixels": l7_data,
        "layer_8_site_structure": l8_data,
        "layer_9_github_signals": l9_data
    }

    # Passages for grounding verification
    state["verified_passages"] = [
        {"passage_id": "p_whois", "source": "WHOIS/RDAP", "content": f"Registrar: {l1_data.get('registrar')}, Created: {l1_data.get('creation_date')}"},
        {"passage_id": "p_dns", "source": "DNS", "content": f"Provider: {l2_data.get('email_provider')}, DMARC: {l2_data.get('dmarc', {}).get('policy')}, SPF: {l2_data.get('spf', {}).get('status')}"},
        {"passage_id": "p_net", "source": "Network", "content": f"IPs: {l3_data.get('ip_addresses')}, Open Ports: {l3_data.get('open_ports')}"},
        {"passage_id": "p_headers", "source": "HTTP", "content": f"Server: {l5_data.get('server_banner')}, CDN: {l5_data.get('detected_cdn')}, Hosting: {l5_data.get('hosting_platform')}"},
        {"passage_id": "p_stack", "source": "TechStack", "content": f"CMS: {l6_data.get('cms')}, Frameworks: {l6_data.get('frontend_frameworks')}"},
        {"passage_id": "p_marketing", "source": "Marketing", "content": f"Runs Ads: {l7_data.get('runs_paid_ads')}, Pixels: {l7_data.get('detected_pixels')}"},
        {"passage_id": "p_site", "source": "SiteStructure", "content": f"Title: {l8_data.get('page_title')}, JSON-LD: {l8_data.get('json_ld_types')}"}
    ]

    return state
