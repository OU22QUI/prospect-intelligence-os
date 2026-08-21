"""
Evaluation & Regression Testing Script for Prospect Intelligence OS
Runs full 10-layer OSINT research across a benchmark list of domains, validates outputs,
and generates summary quality metrics (average confidence score, execution speed, layer coverage).
"""
import sys
import os
import json
import time
from typing import List, Dict, Any

from agent.agent import ProspectIntelligenceAgent
from config import OUTPUT_DIR

BENCHMARK_DOMAINS = [
    ("vercel.com", "Vercel"),
    ("stripe.com", "Stripe"),
    ("cloudflare.com", "Cloudflare"),
    ("supabase.com", "Supabase"),
    ("linear.app", "Linear"),
    ("shopify.com", "Shopify"),
    ("datadoghq.com", "Datadog"),
    ("singlegrain.com", "Single Grain"),
    ("smartbugmedia.com", "SmartBug Media"),
    ("gymshark.com", "Gymshark")
]

def run_evaluation(domains: List[tuple] = BENCHMARK_DOMAINS) -> Dict[str, Any]:
    print("=" * 70)
    print(" 🧪 PROSPECT INTELLIGENCE OS — BENCHMARK EVALUATION SUITE")
    print(f" Total Domains to Benchmark: {len(domains)}")
    print("=" * 70)

    agent = ProspectIntelligenceAgent()
    results = []
    start_all = time.time()

    for idx, (dom, name) in enumerate(domains, 1):
        print(f"\n[{idx}/{len(domains)}] 🔬 Evaluating: {dom} ({name})...")
        t0 = time.time()
        try:
            state = agent.run(company_domain=dom, company_name=name)
            elapsed = time.time() - t0
            dossier = state.get("dossier", {})
            confidence = dossier.get("overall_grounding_confidence", 0.0)
            angles_count = len(dossier.get("layer_10_signal_grounded_angles", []))
            
            res_item = {
                "domain": dom,
                "company_name": name,
                "status": "SUCCESS",
                "elapsed_seconds": round(elapsed, 2),
                "confidence_score": confidence,
                "angles_generated": angles_count,
                "email_provider": dossier.get("layer_2_dns_security", {}).get("email_provider", "Unknown"),
                "cms": dossier.get("layer_6_tech_stack", {}).get("cms", "Unknown"),
                "runs_ads": dossier.get("layer_7_marketing_pixels", {}).get("runs_paid_ads", False),
                "public_repos": dossier.get("layer_9_github_signals", {}).get("public_repos", 0)
            }
            results.append(res_item)
            print(f"  ✅ Finished in {elapsed:.2f}s | Confidence: {confidence*100:.0f}% | Angles: {angles_count}")
        except Exception as e:
            elapsed = time.time() - t0
            results.append({
                "domain": dom,
                "company_name": name,
                "status": "ERROR",
                "error_message": str(e),
                "elapsed_seconds": round(elapsed, 2),
                "confidence_score": 0.0,
                "angles_generated": 0
            })
            print(f"  ❌ Failed in {elapsed:.2f}s | Error: {e}")

    total_time = time.time() - start_all
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    avg_confidence = sum(r["confidence_score"] for r in results if r["status"] == "SUCCESS") / max(1, success_count)
    avg_speed = total_time / max(1, len(domains))

    eval_summary = {
        "benchmark_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_evaluated": len(domains),
        "successful_runs": success_count,
        "success_rate_pct": round((success_count / len(domains)) * 100, 2),
        "average_grounding_confidence": round(avg_confidence, 2),
        "total_elapsed_seconds": round(total_time, 2),
        "average_seconds_per_domain": round(avg_speed, 2),
        "results": results
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    summary_path = os.path.join(OUTPUT_DIR, "evaluation_report.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(eval_summary, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print(" 📊 EVALUATION SUMMARY RESULTS")
    print("=" * 70)
    print(f" Success Rate:               {eval_summary['success_rate_pct']}% ({success_count}/{len(domains)})")
    print(f" Average Grounding Score:    {eval_summary['average_grounding_confidence']*100:.0f}%")
    print(f" Average Latency / Domain:   {eval_summary['average_seconds_per_domain']}s")
    print(f" Report Saved:               {summary_path}")
    print("=" * 70)

    return eval_summary

if __name__ == "__main__":
    run_evaluation()
