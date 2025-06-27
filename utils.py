import docx
import PyPDF2
import spacy
import io
import os

# Load SpaCy model (auto-download if not available)
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# --- Text Extraction ---
def extract_text(file):
    ext = file.name.lower()
    if ext.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif ext.endswith(".docx"):
        return extract_text_from_docx(file)
    elif ext.endswith(".txt"):
        return extract_text_from_txt(file)
    else:
        return ""

def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_docx(file):
    try:
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error reading DOCX: {e}"

def extract_text_from_txt(file):
    try:
        return file.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"Error reading TXT: {e}"

# --- Keyword Extraction ---
def extract_keywords(text):
    doc = nlp(text.lower())
    keywords = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return list(set(keywords))

# --- Match Score Calculation ---
def calculate_match_score(resume_text, job_keywords):
    resume_doc = nlp(resume_text.lower())
    resume_words = set(token.lemma_ for token in resume_doc if token.is_alpha and not token.is_stop)
    matched_keywords = resume_words.intersection(set(job_keywords))
    score = round((len(matched_keywords) / len(job_keywords)) * 100, 2) if job_keywords else 0
    return score, list(matched_keywords)
