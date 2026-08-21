"""
Technographics Node
"""
from agent.state import ProspectState
from tools.technographics_tool import ZeroCostTechnographicsTool

def technographics_node(state: ProspectState) -> ProspectState:
    domain = state["company_domain"]
    tool = ZeroCostTechnographicsTool()
    tech_data = tool.scan_domain(domain)
    state["raw_findings"]["technographics"] = tech_data
    return state
