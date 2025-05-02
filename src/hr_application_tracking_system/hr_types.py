from pydantic import BaseModel
from typing import List

class JobDescription(BaseModel):
    job_title: str
    description: str
    skills: str

class Candidate(BaseModel):
    name: str
    email: str
    bio: str
    skills: str

class CandidateKeywords(BaseModel):
    name: str
    email: str
    bio: str
    skills: str
    keywords: str

class MatchingAnalysis(BaseModel):
    name: str
    structured_comparison_summary: str

class ScoredCandidate(BaseModel):
    name: str
    email: str
    skills_score: int
    experience_score: int
    education_score: int
    final_score: int
    reasoning: str
    feedback: str