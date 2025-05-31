#!/usr/bin/env python

# import sys
import os, json, re
from pathlib import Path
import asyncio
from typing import List, Dict

from crewai.flow.flow import Flow, listen, or_, router, start
from pydantic import BaseModel, Field

from crews.hr_jd_parser_crew.hr_jd_parser_crew import HRJDParser     
from crews.hr_summary_crew.hr_sumary_crew import HRSummaryCrew
from crews.hr_score_crew.hr_score_crew import HRScoreCrew
from crews.hr_aggregate_score_crew.hr_aggregate_score_crew import HRAggregatorCrew
from crews.hr_responser_crew.hr_responser_crew import LeadResponseCrew
from hr_types import ScoredCandidateAcrossRounds, ScoredCandidate, CandidateParsed
from tools.read_resume_file import read_resume_file
from tools.save_csv_file import save_tocsv
from tools.combine_scores import combine_candidates_with_scores


class LeadScoreState(BaseModel):
    id: str= ""
    job_input: List[str] = []
    candidates_resumes: List[str] = []
    candidates_parsed: List[CandidateParsed] = []
    candidates_scored: List[ScoredCandidate] = []
    candidates_scored_across_rounds: List[ScoredCandidateAcrossRounds] = []
    final_scores: List[ScoredCandidate] = []
    scored_leads_feedback: str = ""
    output_jd: str = ""
    output_resumes: str = ""

class HRScoreFlow(Flow[LeadScoreState]):
    initial_state = LeadScoreState
    
    @start()
    def load_resumes_and_job_description(self):
        print("reading resumes and job description")
        current_dir = Path(__file__).parent
        resumes_folder = os.path.join(current_dir, "data","resumes")
        jd_folder = os.path.join(current_dir, "data","jobdescription") 
        self.state.output_jd = os.path.join(current_dir, "data","output","summary_jd.txt")
        self.state.output_resumes = os.path.join(current_dir, "data","output","summary_resumes.txt")   
        
        # load resumes and job description
        for filename in os.listdir(resumes_folder):
            filepath = os.path.join(resumes_folder, filename)
            if not filename.lower().endswith(('.pdf', '.docx', '.html')):
                continue
            self.state.candidates_resumes.append(read_resume_file(filepath))

        for filename in os.listdir(jd_folder):
            filepath = os.path.join(jd_folder, filename)
            if not filename.lower().endswith(('.pdf', '.docx', '.html')):
                continue   
            self.state.job_input.append(read_resume_file(filepath))
    
    @listen((load_resumes_and_job_description))
    async def run_summary_on_jd(self):
        print("### parsing job description")
        crew = HRJDParser().crew()
        n=1
        resume_text = self.state.job_input[0]
        result = crew.kickoff(inputs={"id":n, "jd_text": resume_text})
        output_str = result.raw
        data = json.loads(output_str)
        save_tocsv(self.state.output_jd, data)  
    
    @listen((run_summary_on_jd))
    async def run_summary_on_resumes(self):
        print("### parsing candidates's resumes")
        tasks = []

        async def parsing_single_candidate(resume:str, n:int):
            result = await (
                HRSummaryCrew()
                .crew()
                .kickoff_async(
                    inputs={
                        "id": n,
                        "resume_text":resume,
                    }
                )
            )
            self.state.candidates_parsed.append(result.pydantic)
        n = 1
        for resume in self.state.candidates_resumes:
            print("parsing candidate:", n)
            task = asyncio.create_task(parsing_single_candidate(resume,n))
            tasks.append(task)
            n+=1

        candidate_scores = await asyncio.gather(*tasks)
        print("Finished parsing candidate's resumes: ", len(candidate_scores))
        for cantidate in self.state.candidates_parsed:
            print("####")
            print(cantidate.dict())
            save_tocsv(self.state.output_resumes, cantidate.dict())  

    @listen((run_summary_on_resumes))
    async def score_cantidades(self):
        print("### scoring candidates")
        tasks = []

        async def score_single_candidate(candidate: CandidateParsed):
            result = await (
                HRScoreCrew()
                .crew()
                .kickoff_async(
                    inputs={
                        "id": candidate.id,
                        "name": candidate.name,
                        "email": candidate.email,
                        "bio": candidate.bio,
                        "skills": candidate.skills,
                        "keywords": candidate.keywords,
                        "job_description": self.state.output_jd,
                        "additional_instructions": self.state.scored_leads_feedback
                        }
                    )
                )

            self.state.candidates_scored.append(result.pydantic)
           
        n=3
        for i in range(n):
            for candidate in self.state.candidates_parsed:
                print("Scoring candidate:", candidate.name)
                task = asyncio.create_task(score_single_candidate(candidate))
                tasks.append(task)
    
        candidate_scores = await asyncio.gather(*tasks)
        print("Finished scoring leads: ", len(candidate_scores))

        print("\n")
        print("#####################################################################")
        
        print("Here consolidated evaluations by candidates:")
        self.state.candidates_scored_across_rounds = combine_candidates_with_scores(self.state.candidates_scored)
        print('RESULT')
        print(self.state.candidates_scored_across_rounds)

    @listen((score_cantidades)) ### start last agent
    async def aggregate_cantidades_scores(self):
        print("### agreggating candidates scores")
        tasks = []

        async def aggregate_single_candidate_score(candidate: ScoredCandidateAcrossRounds):
            result = await (
                HRScoreCrew()
                .crew()
                .kickoff_async(
                    inputs={
                        "id": candidate.id,
                        "name": candidate.name,
                        "email": candidate.email,
                        "skills_score": candidate.skills_score,
                        "experience_score": candidate.experience_score,
                        "education_score": candidate.education_score,
                        "final_score": candidate.final_score,
                        "reasoning": candidate.reasoning,
                        "feedback": candidate.feedback
                        }
                    )
                )

            self.state.final_scores.append(result.pydantic)
           
        for candidate in self.state.candidates_scored_across_rounds:
            print("aggregating candidate score:", candidate.name)
            task = asyncio.create_task(aggregate_single_candidate_score(candidate))
            tasks.append(task)

        candidate_scores = await asyncio.gather(*tasks)
        print("Finished scoring leads: ", len(candidate_scores))

        ### end last agent

        

        
        # print("\n")
        # print("#####################################################################")
        
        # print("Here are the top 3 candidates:")
        # print(self.state.candidates_scored)
        # # Sort the scored candidates by their score in descending order
        # sorted_candidates = sorted(
        #     self.state.candidates_scored, key=lambda c: c.final_score, reverse=True
        # )
        # self.state.candidates_scored = sorted_candidates
        # print(self.state.candidates_scored)

         # Select the top 3 candidates
        # top_candidates = sorted_candidates[:3]

        # for candidate in top_candidates:
        #     print(
        #         f"ID: {candidate.id}, Name: {candidate.name}, Score: {candidate.final_score}, Reason: {candidate.reasoning}"
        #     )


def kickoff():
    """
    Run the flow.
    """
    hr_score_flow = HRScoreFlow()
    hr_score_flow.kickoff()

if __name__ == "__main__":
    kickoff()
