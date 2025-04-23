# hr_application_tracking_system/utils.py
from docx import Document
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

def read_resume_file(filepath):
    ext = filepath.lower().split('.')[-1]
    
    if ext == 'pdf':
        reader = PdfReader(filepath)
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    
    elif ext == 'docx':
        doc = Document(filepath)
        return "\n".join(p.text for p in doc.paragraphs)

    elif ext == 'html':
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup.get_text()
    
    else:
        raise ValueError(f"Unsupported file format: {ext}")
