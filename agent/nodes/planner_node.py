"""
Planner Node - Formulates 10-Layer Research Plan
"""
from agent.state import ProspectState, ResearchTask

def planner_node(state: ProspectState) -> ProspectState:
    domain = state["company_domain"]
    name = state.get("company_name") or domain.split(".")[0].capitalize()

    tasks = [
        ResearchTask(id="L1", category="identity", description=f"WHOIS/RDAP registry scan for {domain}").model_dump(),
        ResearchTask(id="L2", category="dns_security", description=f"DNS topology, SPF, DMARC, DKIM audit for {domain}").model_dump(),
        ResearchTask(id="L3", category="network_infra", description=f"Network IP resolution & Shodan InternetDB audit for {domain}").model_dump(),
        ResearchTask(id="L4", category="ssl_cert", description=f"SSL/TLS handshake & cert transparency for {domain}").model_dump(),
        ResearchTask(id="L5", category="headers_cdn", description=f"HTTP headers, server banner, CDN & security score for {domain}").model_dump(),
        ResearchTask(id="L6", category="tech_stack", description=f"CMS, frontend frameworks & UI library scanner for {domain}").model_dump(),
        ResearchTask(id="L7", category="marketing", description=f"Ad pixel & tracking infrastructure detection for {domain}").model_dump(),
        ResearchTask(id="L8", category="site_structure", description=f"Meta tags, OpenGraph, JSON-LD Schema & robots/sitemap for {domain}").model_dump(),
        ResearchTask(id="L9", category="github_dev", description=f"Public GitHub org & language telemetry for {name}").model_dump(),
        ResearchTask(id="L10", category="synthesis", description=f"Synthesize 10-layer dossier & generate 3 signal-grounded angles").model_dump(),
    ]

    state["company_name"] = name
    state["todos"] = tasks
    state["step_count"] = state.get("step_count", 0) + 1
    return state
