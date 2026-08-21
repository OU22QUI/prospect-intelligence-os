"""
Hiring & Friction Node
"""
from agent.state import ProspectState
from tools.public_data_tool import ZeroCostPublicDataTool

def hiring_friction_node(state: ProspectState) -> ProspectState:
    company_name = state["company_name"]
    clean_org = company_name.lower().replace(" ", "").replace("-", "")
    tool = ZeroCostPublicDataTool()
    gh_data = tool.fetch_github_org_data(clean_org)
    state["raw_findings"]["hiring_friction"] = {"github_signals": gh_data, "hiring_results": [], "friction_results": []}
    return state
