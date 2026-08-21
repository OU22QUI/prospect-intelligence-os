"""
Ownership & Execs Node
"""
from agent.state import ProspectState

def ownership_execs_node(state: ProspectState) -> ProspectState:
    state["raw_findings"]["ownership_execs"] = {
        "corporate_registration": {"jurisdiction": "Active Entity", "company_number": "N/A", "status": "Active"},
        "sec_filings": {"cik": "N/A"},
        "executive_profiles": []
    }
    return state
