"""
Ad Pixels Node
"""
from agent.state import ProspectState
from tools.ad_pixels_tool import ZeroCostAdPixelsTool

def ad_pixels_node(state: ProspectState) -> ProspectState:
    domain = state["company_domain"]
    tool = ZeroCostAdPixelsTool()
    pixels_data = tool.detect_pixels(domain)
    state["raw_findings"]["ad_pixels"] = pixels_data
    return state
