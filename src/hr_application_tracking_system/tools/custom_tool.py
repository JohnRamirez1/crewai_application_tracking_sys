from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
    


### edit tool to use

from crewai import Agent, Crew, Task, Knowledge
from docx import Document
import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    return "\n".join(page.get_text() for page in doc)

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)

# Load content
resume_text = extract_text_from_pdf("files/resume.pdf")
job_text = extract_text_from_docx("files/job_description.docx")

# Wrap into knowledge
resume_knowledge = Knowledge(content=resume_text)
job_knowledge = Knowledge(content=job_text)

# Define agents/tasks and pass knowledge
agent = Agent(...)  # your resume_parser agent
task = Task(description="Extract structured info", agent=agent, knowledge=resume_knowledge)
crew = Crew(tasks=[task], agents=[agent])
crew.run()

