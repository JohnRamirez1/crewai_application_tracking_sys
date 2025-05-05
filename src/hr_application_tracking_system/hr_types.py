from pydantic import BaseModel
from typing import List


class JobDescription(BaseModel):
    id: int
    job_title: str
    description: str
    skills: str

class Candidate(BaseModel):
    id: int
    name: str
    email: str
    bio: str
    skills: str

class CandidateParsed(BaseModel):
    id: int
    name: str
    email: str
    bio: str
    skills: str
    keywords: str


class MatchingAnalysis(BaseModel):
    id: int
    name: str
    structured_comparison_summary: str

class ScoredCandidate(BaseModel):
    id: int
    name: str
    email: str
    skills_score: int
    experience_score: int
    education_score: int
    final_score: int
    reasoning: str
    feedback: str