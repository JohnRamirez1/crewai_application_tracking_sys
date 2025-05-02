#!/usr/bin/env python

# import sys
import warnings, os, csv, json, shutil
from pathlib import Path
from crews.hr_summary_crew.hr_sumary_crew import HRSummaryCrew
from crews.hr_jd_parser_crew.hr_jd_parser_crew import HRJDParser     
from tools.read_resume_file import read_resume_file


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run_summary_on_jd(resume_folder: str, output_csv: str):
    crew = HRJDParser().crew()
    n=1
    for filename in os.listdir(resume_folder):
        filepath = os.path.join(resume_folder, filename)
        if not filename.lower().endswith(('.pdf', '.docx', '.html')):
            continue

        resume_text = read_resume_file(filepath)
        result = crew.kickoff(inputs={"resume_text": resume_text})
        output_str = result.raw
        data = json.loads(output_str)
        data = {"id": n, **data}  # Prepend ID
        
        # write to CSV
        with open(output_csv, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if file.tell() == 0:
                writer.writeheader()  # only write header if file is new/empty
            writer.writerow(data)

def run_summary_on_resumes(resume_folder: str, output_csv: str):
    crew = HRSummaryCrew().crew()
    
    n=1
    for filename in os.listdir(resume_folder):
        filepath = os.path.join(resume_folder, filename)
        if not filename.lower().endswith(('.pdf', '.docx', '.html')):
            continue

        resume_text = read_resume_file(filepath)
        result = crew.kickoff(inputs={"resume_text": resume_text})
        output_str = result.raw
        data = json.loads(output_str)
        data = {"id": n, **data}  # Prepend ID
        
        # write to CSV
        with open(output_csv, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if file.tell() == 0:
                writer.writeheader()  # only write header if file is new/empty
            writer.writerow(data)
        n+=1

if __name__ == "__main__":
    
    # parser resumes
    output_jd  = Path("output_jd")
    output_resumes  = Path("output_resumes")
    if output_resumes.exists() and output_resumes.is_dir():
        shutil.rmtree(output_resumes)
    if output_jd.exists() and output_jd.is_dir():
        shutil.rmtree(output_jd)
    Path(output_jd).mkdir(exist_ok=True)
    Path(output_resumes).mkdir(exist_ok=True)
    
    resume_folder = "data/resumes"
    jd_folder = "data/jd"
    output_resumes_csv = os.path.join(output_resumes,"summary_resumes.txt")
    output_jd_csv = os.path.join(output_jd,"summary_jd.txt")
    
    run_summary_on_resumes(resume_folder, output_resumes_csv)
    run_summary_on_jd(jd_folder, output_jd_csv)
