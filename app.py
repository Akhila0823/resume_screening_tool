import streamlit as st
from utils import extract_text, extract_keywords, calculate_match_score

# ✅ Set page configuration (must be first)
st.set_page_config(page_title="Resume Screening Tool", page_icon="📄", layout="wide")

# --- Sidebar ---
st.sidebar.title("🔧 Input")
job_description = st.sidebar.text_area("Paste Job Description Here", height=300)

uploaded_files = st.sidebar.file_uploader(
    "📤 Upload Resumes (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

# --- Main Title ---
st.title("📄 AI Resume Screening Tool")

# --- Check if inputs exist ---
if job_description and uploaded_files:
    with st.spinner("Analyzing resumes..."):
        job_keywords = extract_keywords(job_description)
        matched = []

        for resume in uploaded_files:
            try:
                text = extract_text(resume)
                resume_keywords = extract_keywords(text)
                match_score, matched_keywords = calculate_match_score(job_keywords, resume_keywords)

                matched.append({
                    "filename": resume.name,
                    "score": match_score,
                    "keywords": matched_keywords,
                })
            except Exception as e:
                st.error(f"Error processing {resume.name}: {e}")

    # --- Display Results ---
    if matched:
        # 🔽 Sort by match score descending
        matched = sorted(matched, key=lambda x: x["score"], reverse=True)

        st.markdown("## 📊 Results (Sorted by Match Score):")
        for res in matched:
            st.markdown(f"### 🧾 {res['filename']}")
            st.markdown(
                f"<h2 style='color:#4CAF50; font-size: 36px;'>Match Score: {res['score']:.2f}%</h2>",
                unsafe_allow_html=True,
            )
            st.progress(res['score'] / 100)
            st.write(f"**Matched Keywords ({len(res['keywords'])}):** {', '.join(res['keywords'])}")
            st.markdown("---")
    else:
        st.warning("No valid resumes processed.")
else:
    st.info("Please paste a job description and upload one or more resumes.")
