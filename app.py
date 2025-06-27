import streamlit as st
import pandas as pd
from utils import extract_text, extract_keywords, calculate_match_score

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Resume Screening Tool", page_icon="📄", layout="wide")
st.title("📄 AI Resume Screening Tool")

# --- SIDEBAR INPUT ---
st.sidebar.header("📝 Job Description & Resume Upload")

job_desc = st.sidebar.text_area(
    "Paste Job Description",
    height=300,
    placeholder="Paste the full job description here...",
    help="This will be used to extract keywords for matching."
)

uploaded_files = st.sidebar.file_uploader(
    "📤 Upload Resumes (PDF, DOCX, TXT)",
    accept_multiple_files=True,
    type=["pdf", "docx", "txt"]
)

# --- SCREENING LOGIC ---
if job_desc and uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded. Analyzing resumes...")

    job_keywords = extract_keywords(job_desc)
    results = []

    for resume in uploaded_files:
        text = extract_text(resume)
        score, matched_keywords = calculate_match_score(text, job_keywords)
        results.append({
            "name": resume.name,
            "score": score,
            "matched_keywords": matched_keywords
        })

    # Sort by score descending
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    st.subheader(f"📊 Results: {len(results)} resumes analyzed")

    # --- CSV DOWNLOAD ---
    df = pd.DataFrame([
        {
            "Resume": r["name"],
            "Match Score (%)": r["score"],
            "Matched Keywords": ", ".join(sorted(r["matched_keywords"]))
        }
        for r in results
    ])
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="resume_screening_results.csv",
        mime="text/csv"
    )

    # --- SHOW RESULTS ---
    for result in results:
        color_label = (
            "✅ High Match" if result["score"] >= 70 else
            "⚠️ Medium Match" if result["score"] >= 40 else
            "❌ Low Match"
        )
        st.markdown(f"### 🧾 {result['name']} — {color_label}")
        st.progress(result["score"] / 100)
        st.metric("Match Score", f"{result['score']}%", delta=f"{len(result['matched_keywords'])} keywords")
        with st.expander("🔍 View Matched Keywords"):
            st.write(", ".join(sorted(result['matched_keywords'])) if result['matched_keywords'] else "No keywords matched.")
        st.markdown("---")

elif not job_desc:
    st.info("⬅️ Please paste a job description to begin.")
elif not uploaded_files:
    st.info("⬅️ Upload one or more resumes to analyze.")
