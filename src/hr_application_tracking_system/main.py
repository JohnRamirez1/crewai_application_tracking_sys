#!/usr/bin/env python

# import sys
import warnings
import os
import csv
from pathlib import Path
from crews.hr_summary_crew.hr_sumary_crew import HRSummaryCrew     
from tools.read_resume_file import read_resume_file

# from datetime import datetime
# from hr_application_tracking_system.crew import HrApplicationTrackingSystem

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run_summary_on_resumes(resume_folder: str, output_csv: str):
    crew = HRSummaryCrew().crew()
    candidate_summaries = []

    for filename in os.listdir(resume_folder):
        filepath = os.path.join(resume_folder, filename)
        if not filename.lower().endswith(('.pdf', '.docx', '.html')):
            continue

        resume_text = read_resume_file(filepath)
        result = crew.kickoff(inputs={"resume_text": resume_text})
        print(result)
        file_path = "output/results.txt"

        # Open the file in append mode and write
        with open(file_path, 'a', encoding='utf-8') as f:
             f.write(str(result) + '\n')  # convert to string

if __name__ == "__main__":
    resume_folder = "data/resumes"       # Put your resume files here
    output_csv = "data/resume_summary.csv"
    Path("output").mkdir(exist_ok=True)
    run_summary_on_resumes(resume_folder, output_csv)
