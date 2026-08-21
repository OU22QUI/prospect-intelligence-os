# 🎯 Prospect Intelligence OS

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Framework: LangGraph](https://img.shields.io/badge/Framework-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Zero-Cost Stack: $0 APIs](https://img.shields.io/badge/Zero--Cost-No%20Paid%20APIs-success.svg)]()
[![Schema: v1.0.0](https://img.shields.io/badge/Schema-v1.0.0-purple.svg)](schemas/dossier_v1.json)

> **Infrastructure-grade 10-layer OSINT research agent & signal synthesis engine.**  
> Autonomous technical profiling, DNS deliverability auditing, network fingerprinting, and signal-grounded intelligence synthesis—using only free, zero-cost public data sources.

---

## ⚡ Why Prospect Intelligence OS?

Most B2B account intelligence tools force developers and revenue teams into expensive recurring credit models ($500–$3,000/month) to query basic technographics, DNS records, and website metadata.

**Prospect Intelligence OS** is a self-hosted, local-first research primitive that reconstructs comprehensive company intelligence for **$0/month** by coordinating 10 specialized open-source scanners across DNS, WHOIS/RDAP, HTTP response headers, DOM signatures, certificate transparency, and public developer APIs.

---

## 📊 Feature Comparison: Prospect Intelligence OS vs. Legacy Data Vendors

| Capability / Feature | **Prospect Intelligence OS** | **Clay.com** | **ZoomInfo** | **BuiltWith** |
|---|---|---|---|---|
| **Monthly Subscription Cost** | **$0 / month (Free & Open Source)** | $149 – $800+/mo | $15,000 – $35,000/yr | $295 – $495/mo |
| **API Credit Limits** | **Unlimited (Self-Hosted)** | Strict credit burn per query | Strict credit burn per query | 2,000 lookups/mo |
| **Data Architecture** | **Local-First / Sovereign** | Third-party cloud SaaS | Closed database vendor | Cloud lookup API |
| **DNS & Deliverability Posture Audit** | ✅ **SPF syntax, DMARC policy, DKIM, IPv6** | ⚠️ Partial (via paid integrations) | ❌ None | ❌ None |
| **Network & Port Surface (Shodan InternetDB)**| ✅ **Open ports, CPEs, CVEs** | ❌ None | ❌ None | ❌ None |
| **SSL/TLS & Cert Transparency** | ✅ **TLS version, issuer, SANs, cipher** | ❌ None | ❌ None | ❌ None |
| **Security Headers Posture Score** | ✅ **HSTS, CSP, X-Frame, Referrer (0-100)**| ❌ None | ❌ None | ❌ None |
| **Ad Pixels & Analytics Stack** | ✅ **Meta, Google Ads, LinkedIn, TikTok** | ⚠️ Paid enrichment step | ❌ None | ✅ Yes |
| **Public GitHub Dev Velocity** | ✅ **Public repos, language breakdown** | ⚠️ Paid enrichment step | ❌ None | ❌ None |
| **Factual Grounding Engine (FPG)** | ✅ **Evidence passage verification** | ❌ None | ❌ None | ❌ None |
| **Signal-Grounded Outreach Angles** | ✅ **3 factual hooks per account** | ⚠️ Generic prompt templates | ❌ None | ❌ None |

---

## 🔬 The 10-Layer Research Stack

```
Target Domain ──► [ Planner Node ]
                        │
                        ▼
 ┌────────────────────────────────────────────────────────┐
 │  Layer 1: Identity & WHOIS / RDAP Registration        │
 │  Layer 2: DNS Topology & Deliverability Posture        │
 │  Layer 3: Network Infrastructure & Shodan InternetDB   │
 │  Layer 4: SSL/TLS & Certificate Transparency           │
 │  Layer 5: Web Server, Hosting & Security Headers Score │
 │  Layer 6: Technology Stack & Framework Fingerprinting  │
 │  Layer 7: Marketing, Analytics & Ad Pixels Detection   │
 │  Layer 8: Site Architecture, SEO & JSON-LD Schemas     │
 │  Layer 9: Developer Velocity & Public GitHub Telemetry │
 └──────────────────────┬─────────────────────────────────┘
                        │
                        ▼
             [ FPG Verifier Node ]
             (Cross-check evidence)
                        │
                        ▼
            [ Synthesizer Node ]
     (Layer 10: 3 Signal-Grounded Angles)
                        │
                        ▼
         Structured JSON + Markdown Dossier
```

For full technical specifications on all 10 layers, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 🚀 Quickstart

### Option A: Local Python Environment

```bash
# 1. Clone the repository
git clone https://github.com/your-org/prospect-intelligence-os.git
cd prospect-intelligence-os

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run CLI on any target company domain
python -m agent.runner vercel.com "Vercel"
```

Output generated:
- `output/prospect_dossier_vercel_com.json` (Structured machine-readable data)
- `output/prospect_dossier_vercel_com.md` (Executive intelligence report)

### Option B: Docker / Docker Compose

```bash
# Start the REST API container
docker-compose up -d

# API is live at http://localhost:8000
curl -X POST http://localhost:8000/api/research \
     -H "Content-Type: application/json" \
     -d '{"domain": "cloudflare.com"}'
```

Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

---

## 🧪 Benchmark Evaluation Suite

Run automated regression testing and quality checks across 10 benchmark domains with a single command:

```bash
python evaluate.py
```

Benchmark output produces comprehensive stats:
```
======================================================================
 📊 EVALUATION SUMMARY RESULTS
======================================================================
 Success Rate:               100.0% (10/10)
 Average Grounding Score:    92%
 Average Latency / Domain:   12.42s
 Report Saved:               output/evaluation_report.json
======================================================================
```

---

## 📑 Production Example Dossiers

Real, unedited dossiers produced by the engine are available in the [`examples/`](examples/) directory:

- 🌐 **[Vercel Dossier (`examples/vercel_dossier.md`)](examples/vercel_dossier.md)** — Cloud SaaS & Developer Platform (`95% Grounding Confidence`)
- 🛡️ **[Cloudflare Dossier (`examples/cloudflare_dossier.md`)](examples/cloudflare_dossier.md)** — Global Enterprise Infrastructure (`96% Grounding Confidence`)
- 📈 **[SmartBug Media Dossier (`examples/smartbugmedia_dossier.md`)](examples/smartbugmedia_dossier.md)** — B2B Growth Agency (`93% Grounding Confidence`)

---

## 💡 Example Signal-Grounded Angles Preview

Every research run produces **3 distinct, factual outreach angles** derived strictly from verified technical and strategic triggers:

```markdown
### Angle 1: Infrastructure Integration & Mail Flow
- **Trigger:** Domain operates on Custom / Self-Hosted Mail Server with strict DMARC REJECT policy (k1, s1 selectors).
- **Thesis:** Hardened mail security postures require zero-friction DKIM/SPF alignment when integrating external workflow automation.
- **Suggested Hook:** *"Noticed Cloudflare maintains a hardened Custom / Self-Hosted Mail Server setup with strict DMARC REJECT enforcement. When connecting external data or enrichment tooling into your workflow, how do you handle DKIM selector alignment without compromising sender reputation?"*

### Angle 2: Analytics Stack & Data Pipeline Enrichment
- **Trigger:** Marketing and analytics event routing detected: Google Tag Manager, HubSpot Marketing.
- **Thesis:** Modern customer data pipelines benefit from passing raw technographic signals directly into event streams rather than relying on static form fills.
- **Suggested Hook:** *"Noticed Cloudflare's web setup routes events through Google Tag Manager, HubSpot Marketing. Are you currently enriching incoming lead events with live technographic/DNS signals at the data layer, or relying mostly on form inputs?"*

### Angle 3: Developer Velocity & Technical Stack
- **Trigger:** Active public GitHub organization with 574 public repositories (primary languages: TypeScript, Go).
- **Thesis:** High public engineering velocity indicates a developer-first culture that values structured JSON schemas and API-first tooling.
- **Suggested Hook:** *"Noticed Cloudflare's GitHub org has 574 public repos with heavy TypeScript, Go activity. Is your engineering team maintaining custom internal scrapers for account intelligence, or leveraging structured schema-validated APIs?"*
```

---

## 📜 Commercial Interface Contract

For downstream control planes, CRMs, or ETL pipelines consuming these research results, a versioned JSON schema is defined at:
- **Schema Specification:** [`schemas/dossier_v1.json`](schemas/dossier_v1.json)
- **Integration Guide:** [`schemas/README.md`](schemas/README.md)

---

## ⚠️ Known Limitations

| Limitation | Details |
|---|---|
| **Free endpoint rate limits** | Shodan InternetDB, GitHub Org API, and RDAP registries impose rate limits. Batch runs exceeding ~50–100 domains in rapid succession may experience throttling or temporary 429 responses. The agent handles these gracefully but results may be incomplete. |
| **WAF / bot-protection blocks** | Domains behind aggressive WAFs (Cloudflare Under Attack mode, Akamai Bot Manager, PerimeterX) may return empty or challenge pages for Layers 5–8 (HTTP headers, tech stack, ad pixels, site structure). Grounding confidence will reflect this transparently. |
| **GitHub org name inference** | Layer 9 infers the GitHub organization name from the company name. For companies whose GitHub org differs significantly from their trade name (e.g. `meta` vs `facebook`), detection may fail. The output will report `0 public repos` rather than hallucinate. |
| **No contact or people data** | This module profiles **companies and domains**, not individuals. It does not discover email addresses, phone numbers, LinkedIn profiles, or org charts. Contact enrichment belongs to commercial layers. |
| **DOM-dependent layers require JavaScript-rendered content** | Layers 6–8 parse raw HTML responses. Single-page apps that render entirely via client-side JavaScript (e.g. pure React SPAs without SSR) may show reduced tech stack and pixel detection accuracy. |
| **WHOIS privacy masking** | Many registrars now redact registrant details under GDPR/ICANN privacy policies. Layer 1 will report `Unknown` for masked fields rather than fabricate data. |
| **No historical or longitudinal tracking** | Each research run produces a point-in-time snapshot. The agent does not track changes over time or maintain diff histories across runs. |

---

## 🛡️ Scope & Boundaries

This repository is **strictly an infrastructure-grade research and account intelligence module**. It does **not** include email senders, warmup meshes, inbox rotators, or outbound sequencers.

For an explanation of the commercial control plane boundary, see [CONTROL_PLANE.md](CONTROL_PLANE.md).

---

## 📄 License

Distributed under the **Apache 2.0 License**. See [LICENSE](LICENSE) for more information.
