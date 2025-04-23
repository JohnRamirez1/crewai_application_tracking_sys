from pydantic import BaseModel
from typing import List

class JobDescription(BaseModel):
    job_title: str
    description: str
    skills: str

class Candidate(BaseModel):
    id: str
    name: str
    email: str
    bio: str
    skills: str

class CandidateKeywords(BaseModel):
    id: str
    name: str
    keywords: str

class CandidateMatch(BaseModel):
    id: str
    name: str
    structured_comparison_summary: str


class Criteria(BaseModel):
    name: str
    description: str
    weight: float
    justification: str

class CriteriaDefinition(BaseModel):
    criterias: List[Criteria]

class ScoreDefinition(BaseModel):
    criterion: str
    weight: str
    score: int
    reasoning: str

class CandidateScore(BaseModel):
    id: str
    name: str
    scores: List[ScoreDefinition]
    final_score: str
    reason: str


class ScoredCandidate(BaseModel):
    id: str
    name: str
    email: str
    bio: str
    skills: str
    final_score: int
    reasoning: str
    feedback: str