"""
FastAPI Server for Prospect Intelligence OS (10-Layer Pure Research Module)
Exposes research endpoints for single-domain analysis and dossier retrieval.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sqlite3
import json
import os

from agent.agent import ProspectIntelligenceAgent
from config import DB_PATH

app = FastAPI(
    title="Prospect Intelligence OS API",
    description="Open-source, infrastructure-grade 10-layer OSINT research agent for company profiling and signal-grounded intelligence.",
    version="1.0.0"
)

agent = ProspectIntelligenceAgent()

class ResearchRequest(BaseModel):
    domain: str
    company_name: Optional[str] = None

@app.get("/")
def health():
    return {
        "status": "online",
        "module": "Prospect Intelligence OS",
        "version": "1.0.0",
        "description": "Infrastructure-Grade 10-Layer OSINT Research Agent"
    }

@app.post("/api/research")
def conduct_research(req: ResearchRequest):
    if not req.domain or "." not in req.domain:
        raise HTTPException(status_code=400, detail="A valid company domain is required (e.g. 'vercel.com').")
    
    clean_domain = req.domain.strip().lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
    
    try:
        state = agent.run(company_domain=clean_domain, company_name=req.company_name)
        dossier = state.get("dossier", {})
        return {
            "status": "success",
            "domain": clean_domain,
            "grounding_confidence": dossier.get("overall_grounding_confidence", 0.9),
            "dossier": dossier
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research agent execution failed: {str(e)}")

@app.get("/api/dossier/{domain}")
def get_stored_dossier(domain: str):
    clean_domain = domain.strip().lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
    
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=404, detail="Database not initialized yet.")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT company_name, confidence_score, dossier_json, created_at FROM prospect_dossiers WHERE domain=?", (clean_domain,))
    row = c.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"No dossier found for domain '{clean_domain}'.")

    return {
        "domain": clean_domain,
        "company_name": row[0],
        "confidence_score": row[1],
        "created_at": row[3],
        "dossier": json.loads(row[2])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.server:app", host="127.0.0.1", port=8000, reload=True)
