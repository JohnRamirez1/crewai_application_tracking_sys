from typing import List, Dict
from hr_types import ScoredCandidateAcrossRounds, ScoredCandidate

def combine_candidates_with_scores( candidate_evaluation: List[ScoredCandidate]
        ) -> List[ScoredCandidateAcrossRounds]:
    """
    bind candidates scores into one List of dictionaries
    """
    # print("COMBINING CANDIDATES WITH SCORES")
    # print("SCORES:", candidate_evaluation)
    # Create a dictionary to map score IDs to their corresponding CandidateScore objects
    merged: Dict[int, Dict] = {}

    for cand_dict in candidate_evaluation:
        cand = cand_dict
        if cand.id not in merged:
            merged[cand.id] = {
                "id": cand.id,
                "name": cand.name,
                "email": cand.email,
                "skills_score": [],
                "experience_score": [],
                "education_score": [],
                "final_score": [],
                "reasoning": [],
                "feedback": []
            }
        merged[cand.id]["skills_score"].append(cand.skills_score)
        merged[cand.id]["experience_score"].append(cand.experience_score)
        merged[cand.id]["education_score"].append(cand.education_score)
        merged[cand.id]["final_score"].append(cand.final_score)
        merged[cand.id]["reasoning"].append(cand.reasoning)
        merged[cand.id]["feedback"].append(cand.feedback)
    
    # print("GROUPED SCORES:", candidate_evaluation)

    return [ScoredCandidateAcrossRounds(**data) for data in merged.values()]
    