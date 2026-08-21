"""
Website Deep Node
"""
from agent.state import ProspectState
from tools.website_deep_tool import ZeroCostWebsiteDeepTool
from tools.whois_tool import ZeroCostWhoisTool

def website_deep_node(state: ProspectState) -> ProspectState:
    domain = state["company_domain"]
    
    site_tool = ZeroCostWebsiteDeepTool()
    whois_tool = ZeroCostWhoisTool()
    
    site_data = site_tool.scan_site(domain)
    whois_data = whois_tool.lookup(domain)
    
    state["raw_findings"]["website_deep"] = {
        "website_metadata": site_data,
        "whois_registration": whois_data
    }
    
    passages = state.get("verified_passages", [])
    passages.append({
        "passage_id": "p_website_deep",
        "source_url": f"https://{domain}",
        "content": f"Title: {site_data.get('page_title')} | Registrar: {whois_data.get('registrar')}"
    })
    state["verified_passages"] = passages
    return state
