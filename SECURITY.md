# 🔒 Security Policy

## 📋 Scope & Intended Use

**Prospect Intelligence OS** is designed exclusively as an **OSINT research and technical profiling module** that queries public, authoritative endpoints (such as DNS root servers, public WHOIS/RDAP registries, and HTTP response headers).

It is intended for legitimate market research, security posture evaluation, and technical account intelligence. It does not perform active vulnerability exploitation, denial-of-service testing, or unauthorized credential access.

---

## 🛡️ Reporting a Security Vulnerability

If you discover a security vulnerability or potential exploit within Prospect Intelligence OS, please report it responsibly:

1. **Do not create a public GitHub issue.**
2. Send an email describing the vulnerability, steps to reproduce, and potential impact to `security@prospectintelligence.dev` (or open a private GitHub Security Advisory).
3. We will acknowledge receipt within **48 hours** and provide a patch timeline.

---

## ⚙️ Safe Querying Guidelines

- Always respect target server `robots.txt` directives.
- Adhere to rate limits and polite request timeouts when querying public APIs.
- Use dedicated non-production IPs when executing large-scale batch research jobs.
