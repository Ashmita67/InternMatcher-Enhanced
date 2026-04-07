import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_skills(text):
    if not text:
        return []
    
    # A basic predefined list of common skills for demonstration
    common_skills = [
        "python", "java", "c++", "javascript", "react", "node.js", "flask", "django", 
        "sql", "mysql", "mongodb", "aws", "docker", "kubernetes", "machine learning", 
        "data analysis", "html", "css", "git", "linux", "c#", "php", "ruby", "swift",
        "kotlin", "typescript", "angular", "vue", "spring", "express", "postgresql",
        "oracle", "redis", "elasticsearch", "azure", "gcp", "tensorflow", "pytorch",
        "pandas", "numpy", "scikit-learn", "matlab", "r", "c", "go", "rust", "dart",
        "flutter", "react native", "excel", "word", "powerpoint", "communication",
        "leadership", "project management", "agile", "scrum", "jira", "confluence"
    ]
    
    found_skills = set()
    text_lower = text.lower()
    
    # Simple keyword matching
    for skill in common_skills:
        # Use lookarounds instead of \b to properly handle skills ending/starting with non-word characters like c++ or c#
        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
    return list(found_skills)
