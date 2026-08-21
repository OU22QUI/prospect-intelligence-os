"""
State Definition & Data Models for Prospect Intelligence OS (10-Layer Pure Research)
"""
from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ResearchTask(BaseModel):
    id: str
    category: str
    description: str
    completed: bool = False
    result: Optional[Dict[str, Any]] = None

class GroundedPassage(BaseModel):
    passage_id: str
    source_url: str
    content: str
    extracted_at: str = Field(default_factory=lambda: "")

class ProspectState(TypedDict):
    company_domain: str
    company_name: str
    todos: List[Dict[str, Any]]
    raw_findings: Dict[str, Any]
    verified_passages: List[Dict[str, Any]]
    confidence_scores: Dict[str, float]
    dossier: Dict[str, Any]
    errors: List[str]
    step_count: int
