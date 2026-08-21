# 🤝 Contributing to Prospect Intelligence OS

Thank you for your interest in contributing to **Prospect Intelligence OS**!

---

## 🧭 Guiding Philosophy

Prospect Intelligence OS is strictly an **infrastructure-grade research and account intelligence module**. 

We welcome contributions that improve:
- Accuracy and reliability of the 10 OSINT scanner layers
- Zero-cost public endpoint parsers (DNS, WHOIS/RDAP, Shodan InternetDB, SSL transparency)
- DOM signature detection for modern frameworks, CMS platforms, and marketing pixels
- Performance, concurrency, and local execution efficiency
- Documentation, architecture diagrams, and test coverage

**Out of Scope for this Repository:**
- Outbound cold-email sequencers or dispatch engines
- Multi-mailbox fleet rotators or warmup automation
- Aggressive directory harvesting or scraping tools that violate target robots.txt/ToS

---

## 🛠️ Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/<your-username>/prospect-intelligence-os.git
cd prospect-intelligence-os

# 2. Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run benchmark evaluation suite
python evaluate.py

# 5. Run single-domain test CLI
python -m agent.runner vercel.com "Vercel"
```

---

## 🧪 Submitting a Pull Request

1. Create a feature branch: `git checkout -b feature/improved-dns-scanner`
2. Commit clear, well-scoped changes adhering to PEP 8 standards.
3. Verify that `python evaluate.py` passes with a **100% success rate** across all benchmark domains.
4. Open a Pull Request with a description of the improvement and sample terminal output.

---

## 📜 License

By contributing to Prospect Intelligence OS, you agree that your contributions will be licensed under its [Apache 2.0 License](LICENSE).
