# 📜 Prospect Intelligence OS: Commercial Interface Contract

> **Schema Specification & Downstream Integration Standard**  
> Version: `v1.0.0` | Schema File: [`dossier_v1.json`](dossier_v1.json)

---

## 1. Purpose & Guiding Contract

This schema defines the **strict, immutable JSON contract** produced by Prospect Intelligence OS. 

Any closed or commercial control plane (such as downstream campaign orchestrators, CRM sync workers, or analytics pipelines) can consume output dossiers adhering to this contract without schema drift or breaking changes.

---

## 2. Key Contract Fields

| Field | Type | Description |
|---|---|---|
| `domain` | `string` | Normalized target root domain (e.g. `vercel.com`). |
| `company_name` | `string` | Inferred or supplied organization display name. |
| `overall_grounding_confidence` | `float` (0.0–1.0) | FPG-weighted evidence confidence score across all 9 research layers. |
| `confidence_breakdown` | `object` | Granular per-layer confidence scores (`layer_1_whois`, `layer_2_dns_security`, etc.). |
| `evidence_provenance` | `object` | Source audit map identifying exact scanner engines and verification status (`VERIFIED`, `PARTIAL`, `NO_DATA`). |
| `layer_1_whois_rdap` to `layer_9_github_signals` | `object` | Raw, unhallucinated technical parameters extracted from authoritative endpoints. |
| `layer_10_signal_grounded_angles` | `array[object]` | Exactly 3 strategic outreach hooks, each containing `pillar`, `factual_trigger`, `angle_thesis`, and `sample_hook`. |

---

## 3. Downstream Consumption Example (Python)

```python
import json
import jsonschema

with open("schemas/dossier_v1.json") as f:
    schema = json.load(f)

# Validate incoming intelligence dossier
with open("output/prospect_dossier_vercel_com.json") as f:
    dossier = json.load(f)

jsonschema.validate(instance=dossier, schema=schema)
print("✅ Dossier conforms 100% to v1 interface contract.")

# Extract signal-grounded hooks safely
for angle in dossier["layer_10_signal_grounded_angles"]:
    print(f"[{angle['pillar']}] Hook: {angle['sample_hook']}")
```

---

## 4. Versioning Policy

- **Minor non-breaking changes** (e.g. adding auxiliary metadata fields) will bump minor versions (`v1.1.0`).
- **Breaking changes** (e.g. altering existing field types or removing layer schemas) will spawn a new schema version (`v2.0.0`).
