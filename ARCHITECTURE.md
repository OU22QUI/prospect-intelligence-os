# 🏛️ Prospect Intelligence OS: System Architecture

> **Infrastructure-Grade 10-Layer OSINT Research & Signal Synthesis Agent**  
> Built with **LangGraph**, **Zero-Cost Public Scanners**, and **Faithful Passage Grounding (FPG)**.  
> Interface Contract: [`schemas/dossier_v1.json`](schemas/dossier_v1.json) (`v1.0.0`)

---

## 1. Architectural Overview

Prospect Intelligence OS is designed as an unopinionated, modular research primitive. It takes a target company domain as input, executes 10 foundational OSINT research layers, computes factual confidence scores, and synthesizes 3 signal-grounded outreach hooks derived exclusively from verified technical signals.

```
                           ┌────────────────────────────────────────────────────────┐
                           │          LangGraph StateGraph Workflow Engine          │
                           └───────────────────────────┬────────────────────────────┘
                                                       │
                                                       ▼
                                            ┌───────────────────────┐
                                            │      Planner Node     │
                                            │  (Task Decomposition) │
                                            └──────────┬────────────┘
                                                       │
                                                       ▼
                                            ┌───────────────────────┐
                                            │  Research Layers Node │
                                            │     (Layers 1 - 9)    │
                                            └──────────┬────────────┘
                                                       │
                                                       ▼
                                            ┌───────────────────────┐
                                            │     Verifier Node     │
                                            │ (FPG Provenance Engine)│
                                            └──────────┬────────────┘
                                                       │
                                                       ▼
                                            ┌───────────────────────┐
                                            │    Synthesizer Node   │
                                            │  (Layer 10 Synthesis) │
                                            └──────────┬────────────┘
                                                       │
                                                       ▼
                                            ┌───────────────────────┐
                                            │      END / Output     │
                                            │   (JSON + Markdown)   │
                                            └───────────────────────┘
```

---

## 2. The 10 Foundational OSINT Layers

| Layer | Component | Scanner Engine | Data Points Extracted |
|---|---|---|---|
| **Layer 1** | **Identity, WHOIS & RDAP** | `WhoisRdapScanner` | Registrar name, domain registration date, domain age, authoritative nameservers, registrant organization. |
| **Layer 2** | **DNS Topology & Deliverability Posture** | `DnsSecurityScanner` | Authoritative MX records, primary email provider (Google Workspace, Microsoft 365, Mimecast, Proofpoint), SPF record syntax & lookup depth, DMARC policy (`p=reject`/`quarantine`/`none`), DKIM selector probing, IPv6 (AAAA) presence, CAA records. |
| **Layer 3** | **Network Infrastructure & Ports** | `NetworkInfraScanner` | A/AAAA IP resolution, reverse DNS hostnames, Shodan InternetDB free endpoint queries (open ports, CPEs, detected CVEs, host tags). |
| **Layer 4** | **SSL/TLS & Certificate Transparency** | `SslCertificateScanner` | SSL handshake state, TLS protocol version (TLSv1.3), cipher suite, certificate issuer organization (Google Trust Services, Let's Encrypt, DigiCert), validity dates, Subject Alternative Names (SANs). |
| **Layer 5** | **Web Server, Hosting & CDN Fingerprint** | `HeadersFingerprintScanner` | Server banner, CDN detection (Cloudflare, Fastly, Akamai, CloudFront), modern hosting platform detection (Vercel, Render, Fly.io), and defensive Security Headers Posture Score (HSTS, CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy). |
| **Layer 6** | **Technology Stack & Frameworks** | `TechStackScanner` | CMS classification (WordPress, Webflow, Shopify, Framer, Ghost, Squarespace), frontend framework detection (Next.js, React, Nuxt.js, Vue, Svelte, Angular), UI libraries (Tailwind CSS, Bootstrap), e-commerce engines. |
| **Layer 7** | **Marketing, Analytics & Ad Pixels** | `ZeroCostAdPixelsTool` | Paid advertising tracking pixels (Meta/Facebook Pixel, Google Ads, LinkedIn Insight Tag, TikTok Pixel), analytics infrastructure (Google Tag Manager, Segment CDP, Hotjar Heatmaps, Klaviyo, HubSpot Marketing). |
| **Layer 8** | **Site Structure, Architecture & SEO Entities** | `SiteStructureScanner` | Page title, meta description, OpenGraph title/description/image, JSON-LD Schema.org graph types (`Organization`, `WebSite`, `Product`, `Article`), core H1/H2 headings, canonical URLs, robots.txt probe, sitemap.xml probe. |
| **Layer 9** | **Developer & Engineering Signals** | `ZeroCostPublicDataTool` | Public GitHub organization public repository count, primary programming language distribution (TypeScript, Python, Go, Rust, C#). |
| **Layer 10**| **Signal-Grounded Outreach Angle Generation** | `SignalGroundedAngleGenerator` | 3 distinct, non-generic outreach angles derived strictly from verified technical and strategic triggers: (1) Deliverability & Email Security, (2) Paid Media & Growth Synergy, (3) Developer Velocity & Modernization. |

---

## 3. Faithful Passage Grounding (FPG) & Provenance Model

To eliminate LLM hallucinations and ensure data integrity, the system implements a **Deterministic Evidence Verification Model**:

### Grounding Weights & Scoring Matrix

$$\text{Overall Confidence} = \sum_{i=1}^{9} w_i \times \text{Score}_i$$

| Research Layer | Weight ($w_i$) | Verification Condition ($1.00$) | Partial Condition ($0.70-0.85$) | Failure Floor ($0.30-0.50$) |
|---|---|---|---|---|
| **Layer 1: WHOIS/RDAP** | `0.10` | Authoritative registrar + creation date found | Registrar found, creation date privacy masked | Connection timeout / WHOIS blocked |
| **Layer 2: DNS Security** | `0.15` | Valid MX + SPF record + DMARC policy | MX records found without SPF/DMARC | No MX records returned |
| **Layer 3: Network Infra** | `0.10` | IP resolved + Shodan InternetDB ports confirmed | IP resolved, port scan fallback used | Host resolution failed |
| **Layer 4: SSL/TLS** | `0.10` | Valid TLS handshake + verifiable issuer org | Self-signed or unverified cert | Port 443 closed |
| **Layer 5: Headers & CDN** | `0.10` | HTTP 200 + Server banner identified | HTTP redirect / 3xx response | Connection refused |
| **Layer 6: Tech Stack** | `0.10` | DOM framework / CMS signature verified | Generic HTML with no framework meta | Static / empty DOM |
| **Layer 7: Marketing Pixels** | `0.10` | Regex pixel match confirmed in DOM | No active ad pixels detected | Script tags stripped/blocked |
| **Layer 8: Site Structure** | `0.15` | Valid title + JSON-LD Schema.org graph | Title found without JSON-LD schema | Empty HTML body |
| **Layer 9: GitHub Dev** | `0.10` | Public GitHub org with repositories found | No public org found for company name | Rate limited / 404 |

### Claim Provenance

Every output dossier includes an `evidence_provenance` map:
```json
"evidence_provenance": {
  "layer_1_whois": { "source": "RDAP/WHOIS", "status": "VERIFIED" },
  "layer_2_dns_security": { "source": "Authoritative DNS (dnspython)", "status": "VERIFIED" },
  "layer_3_network": { "source": "Socket / Shodan InternetDB", "status": "VERIFIED" },
  "layer_4_ssl_tls": { "source": "Native TLS Handshake Context", "status": "VERIFIED" },
  "layer_5_headers_cdn": { "source": "HTTP Response Headers", "status": "VERIFIED" },
  "layer_6_tech_stack": { "source": "DOM & Script Signature Analysis", "status": "VERIFIED" },
  "layer_7_marketing": { "source": "HTML Pixel Regex Matcher", "status": "VERIFIED" },
  "layer_8_site_structure": { "source": "BeautifulSoup4 HTML/JSON-LD Parser", "status": "VERIFIED" },
  "layer_9_github_dev": { "source": "GitHub Org REST API", "status": "VERIFIED" }
}
```

---

## 4. Modularity & Control Plane Integration

The research primitives in `tools/` and `agent/` are strictly decoupled from storage and presentation logic.
- They can be imported directly as a Python package (`from agent.agent import ProspectIntelligenceAgent`) into any proprietary orchestrator, CRM, or ETL pipeline.
- All state structures adhere to Pydantic v2 schemas (`agent/state.py`) and validate against [`schemas/dossier_v1.json`](schemas/dossier_v1.json).
- SQLite checkpointing is implemented as an optional persistence adapter (`config.DB_PATH`).
