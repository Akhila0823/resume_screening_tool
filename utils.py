import docx
import PyPDF2
import spacy
import io

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file):
    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)
    elif file.name.endswith(".txt"):
        return io.StringIO(file.read().decode("utf-8")).read()
    else:
        return ""

def extract_keywords(text):
    doc = nlp(text.lower())
    return [
        token.text
        for token in doc
        if token.is_alpha and not token.is_stop and len(token.text) > 2
    ]

def calculate_match_score(job_keywords, resume_keywords):
    # Ensure input is a list of words (already extracted via extract_keywords)
    job_keywords = set(job_keywords)
    resume_keywords = set(resume_keywords)

    matched_keywords = list(job_keywords.intersection(resume_keywords))
    match_score = (len(matched_keywords) / len(job_keywords)) * 100 if job_keywords else 0

    return match_score, matched_keywords
