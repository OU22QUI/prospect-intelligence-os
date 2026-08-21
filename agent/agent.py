"""
LangGraph 10-Layer Research Agent Pipeline
Orchestrates Planner -> Multi-Layer OSINT Research -> FPG Verifier -> Dossier Synthesizer.
"""
import os
import sqlite3
import json
from typing import Dict, Any, Optional

from agent.state import ProspectState
from agent.nodes.planner_node import planner_node
from agent.nodes.research_layers_node import research_layers_node
from agent.nodes.verifier_node import verifier_node
from agent.nodes.synthesizer_node import synthesizer_node

from config import DB_PATH

try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

class ProspectIntelligenceAgent:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_sqlite_memory()

    def _init_sqlite_memory(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS prospect_dossiers (
                domain TEXT PRIMARY KEY,
                company_name TEXT,
                confidence_score REAL,
                dossier_json TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def build_graph(self):
        if not LANGGRAPH_AVAILABLE:
            return None

        workflow = StateGraph(ProspectState)
        
        workflow.add_node("planner", planner_node)
        workflow.add_node("research_layers", research_layers_node)
        workflow.add_node("verifier", verifier_node)
        workflow.add_node("synthesizer", synthesizer_node)

        workflow.set_entry_point("planner")

        workflow.add_edge("planner", "research_layers")
        workflow.add_edge("research_layers", "verifier")
        workflow.add_edge("verifier", "synthesizer")
        workflow.add_edge("synthesizer", END)

        return workflow.compile()

    def run(self, company_domain: str, company_name: Optional[str] = None) -> Dict[str, Any]:
        initial_state: ProspectState = {
            "company_domain": company_domain.strip().lower(),
            "company_name": company_name or "",
            "todos": [],
            "raw_findings": {},
            "verified_passages": [],
            "confidence_scores": {},
            "dossier": {},
            "errors": [],
            "step_count": 0
        }

        app = self.build_graph()

        if app:
            final_state = app.invoke(initial_state)
        else:
            s = planner_node(initial_state)
            s = research_layers_node(s)
            s = verifier_node(s)
            final_state = synthesizer_node(s)

        dossier = final_state.get("dossier", {})
        
        # Durable SQLite storage
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO prospect_dossiers 
                (domain, company_name, confidence_score, dossier_json)
                VALUES (?, ?, ?, ?)
            """, (
                company_domain,
                company_name or company_domain,
                dossier.get("overall_grounding_confidence", 0.9),
                json.dumps(dossier, ensure_ascii=False)
            ))
            conn.commit()
            conn.close()
        except Exception:
            pass

        return final_state
