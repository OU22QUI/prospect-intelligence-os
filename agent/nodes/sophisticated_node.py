"""
Sophisticated Audit Node
"""
from agent.state import ProspectState
from tools.dns_sec_audit import SophisticatedDnsAuditor
from tools.network_port_scanner import SophisticatedNetworkScanner

def sophisticated_node(state: ProspectState) -> ProspectState:
    domain = state["company_domain"]
    
    dns_auditor = SophisticatedDnsAuditor()
    net_scanner = SophisticatedNetworkScanner()
    
    dns_report = dns_auditor.audit_domain(domain)
    net_report = net_scanner.audit_network(domain)
    
    state["raw_findings"]["sophisticated_intel"] = {
        "dns_security_audit": dns_report,
        "network_and_ssl_audit": net_report,
        "sitemap_architecture": {"sitemap_found": False, "sitemap_urls_count": 0, "discovered_paths": []}
    }
    return state
