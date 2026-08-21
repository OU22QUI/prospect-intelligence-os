# 🛡️ Commercial Boundary & Control Plane Notice

> **Scope Clarification & Boundary Definition**  
> This open-source repository represents the standalone **Research & OSINT Primitive Layer** of the Prospect Intelligence architecture.

---

## 1. What This Open-Source Repository Contains

This repository is intentionally limited to:
- **10-Layer OSINT Research & Signal Extraction:** Automated querying of public DNS, WHOIS/RDAP, HTTP headers, DOM structure, SSL/TLS certificates, and public GitHub signals.
- **Factual Grounding & Confidence Scoring:** Evidence passage verification to ensure research accuracy.
- **Signal-Grounded Angle Generation:** Abstracting factual research into 3 strategic conversational hooks.
- **Self-Hosted Local/Docker Execution:** Clean CLI and single-tenant FastAPI endpoints.

---

## 2. What Is Intentionally Excluded (Commercial Control Plane Layer)

The following enterprise, operational, and outbound execution systems are **not included** in this open-source core and belong exclusively to the commercial control plane:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                       COMMERCIAL CONTROL PLANE BOUNDARY                                  │
├───────────────────────────────────┬─────────────────────────────────────────────────────┤
│ 1. Mailbox Fleet Governance       │ Multi-domain DNS pools, IP rotation, reputation     │
│                                   │ tracking, and automated sending caps.               │
├───────────────────────────────────┼─────────────────────────────────────────────────────┤
│ 2. Automated Warmup Mesh          │ Peer-to-peer synthetic inbox warming networks and   │
│                                   │ deliverability aging routines.                      │
├───────────────────────────────────┼─────────────────────────────────────────────────────┤
│ 3. Outbound Sequencer & Delivery  │ SMTP dispatch, cadence scheduling, multi-channel    │
│                                   │ sequencing (Email + LinkedIn + Voice).              │
├───────────────────────────────────┼─────────────────────────────────────────────────────┤
│ 4. Inbound Conversation Intel     │ IMAP reply classification, sentiment tagging,       │
│                                   │ objection handling, and automated meeting booking.  │
├───────────────────────────────────┼─────────────────────────────────────────────────────┤
│ 5. Global Policy & Suppression    │ Enterprise compliance gates, cross-campaign dedupe, │
│                                   │ GDPR/CASL jurisdiction firewalls, and audit logs.   │
├───────────────────────────────────┼─────────────────────────────────────────────────────┤
│ 6. Closed-Loop Machine Learning   │ Continuous ICP centroid retraining from real-world  │
│                                   │ closed-won conversion data and outcome telemetry.   │
├───────────────────────────────────┼─────────────────────────────────────────────────────┤
│ 7. Multi-Tenant Enterprise Auth   │ Role-based access control (RBAC), team workspaces,  │
│                                   │ SSO, and billing metering.                          │
└───────────────────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 3. Guiding Philosophy

- **Zero Spam Infrastructure:** This open-source repository contains zero sending engines, inbox rotators, or aggressive email probing mechanisms. It is strictly an **infrastructure-grade research and account intelligence module**.
- **Clean Separation of Concerns:** Developers can freely embed this research agent into data pipelines, internal CRM enrichment jobs, or security scanning workflows without taking on outbound sending liability.
