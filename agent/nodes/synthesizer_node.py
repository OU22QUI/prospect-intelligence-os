"""
Synthesizer Node - Assembles 10-Layer Structured Intelligence Dossier
Attaches transparent layer confidence scores, claim provenance, and executes Layer 10.
"""
from typing import Dict, Any
from agent.state import ProspectState
from tools.signal_angles import SignalGroundedAngleGenerator

def synthesizer_node(state: ProspectState) -> ProspectState:
    domain = state["company_domain"]
    name = state["company_name"]
    raw = state.get("raw_findings", {})
    scores = state.get("confidence_scores", {})
    provenance = raw.get("_provenance", {})

    dossier = {
        "domain": domain,
        "company_name": name,
        "overall_grounding_confidence": scores.get("overall_grounding", 0.90),
        "confidence_breakdown": scores,
        "evidence_provenance": provenance,
        "layer_1_whois_rdap": raw.get("layer_1_whois_rdap", {}),
        "layer_2_dns_security": raw.get("layer_2_dns_security", {}),
        "layer_3_network_infra": raw.get("layer_3_network_infra", {}),
        "layer_4_ssl_cert": raw.get("layer_4_ssl_cert", {}),
        "layer_5_headers_fingerprint": raw.get("layer_5_headers_fingerprint", {}),
        "layer_6_tech_stack": raw.get("layer_6_tech_stack", {}),
        "layer_7_marketing_pixels": raw.get("layer_7_marketing_pixels", {}),
        "layer_8_site_structure": raw.get("layer_8_site_structure", {}),
        "layer_9_github_signals": raw.get("layer_9_github_signals", {}),
    }

    # Layer 10: Signal-Grounded Outreach Angles
    angle_gen = SignalGroundedAngleGenerator()
    angles = angle_gen.generate_angles(dossier)
    dossier["layer_10_signal_grounded_angles"] = angles

    state["dossier"] = dossier
    return state
