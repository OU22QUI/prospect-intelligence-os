"""
Interactive Showcase Demo Script for Prospect Intelligence OS
Runs high-speed 10-layer research on 2 sample domains and prints a beautiful terminal summary.
"""
import sys
import os
import json
import time

from agent.agent import ProspectIntelligenceAgent

DEMO_DOMAINS = [
    ("vercel.com", "Vercel"),
    ("cloudflare.com", "Cloudflare")
]

def run_demo():
    print("=" * 72)
    print(" 🎯 PROSPECT INTELLIGENCE OS — LIVE SHOWCASE DEMO")
    print(" Infrastructure-Grade 10-Layer OSINT Research & Signal Synthesis")
    print("=" * 72)

    agent = ProspectIntelligenceAgent()

    for idx, (dom, name) in enumerate(DEMO_DOMAINS, 1):
        print(f"\n[{idx}/{len(DEMO_DOMAINS)}] 🚀 Researching Account: {dom} ({name})...")
        t0 = time.time()
        state = agent.run(company_domain=dom, company_name=name)
        elapsed = time.time() - t0

        dossier = state.get("dossier", {})
        conf = dossier.get("overall_grounding_confidence", 0.9) * 100
        l2 = dossier.get("layer_2_dns_security", {})
        l6 = dossier.get("layer_6_tech_stack", {})
        l7 = dossier.get("layer_7_marketing_pixels", {})
        l9 = dossier.get("layer_9_github_signals", {})
        angles = dossier.get("layer_10_signal_grounded_angles", [])

        print(f"\n  ✅ Completed in {elapsed:.2f}s | FPG Grounding Confidence: {conf:.0f}%")
        print(f"  🏢 Discovered Signals:")
        print(f"     • Email Infrastructure: {l2.get('email_provider')} (DMARC: {l2.get('dmarc', {}).get('policy', 'none').upper()})")
        print(f"     • Frontend/CMS Stack:   {l6.get('cms')} / {', '.join(l6.get('frontend_frameworks', [])) or 'Standard DOM'}")
        print(f"     • Marketing Ad Pixels:  {', '.join(l7.get('detected_pixels', [])) or 'None Detected'}")
        print(f"     • GitHub Dev Velocity:  {l9.get('public_repos', 0)} public repos in {', '.join(l9.get('top_languages', [])) or 'N/A'}")

        print(f"\n  💡 Generated Signal-Grounded Angles:")
        for a_idx, a in enumerate(angles, 1):
            print(f"     [{a_idx}] {a.get('pillar')}:")
            print(f"         Trigger: {a.get('factual_trigger')}")
            print(f"         Hook:    \"{a.get('sample_hook')}\"")
        print("-" * 72)

    print("\n✨ DEMO COMPLETE! Full dossiers saved to data/ and output/.")
    print("Run `python -m agent.runner <domain>` to research any other custom company.")

if __name__ == "__main__":
    run_demo()
