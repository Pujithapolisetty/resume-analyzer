import streamlit as st
import fitz  # PyMuPDF
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources
nltk.download("punkt")
nltk.download("stopwords")

# Helper function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Text preprocessing
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english") + list(string.punctuation))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

# Main analyzer function
def analyze_resume(resume_file, job_description):
    resume_text = extract_text_from_pdf(resume_file)
    resume_tokens = preprocess_text(resume_text)
    jd_tokens = preprocess_text(job_description)

    matched_keywords = [word for word in jd_tokens if word in resume_tokens]
    missing_keywords = [word for word in jd_tokens if word not in resume_tokens]
    match_score = (len(matched_keywords) / len(set(jd_tokens))) * 100

    return match_score, matched_keywords, missing_keywords

# Streamlit UI
st.set_page_config(page_title="Resume Analyzer", page_icon="📄")
st.title("📄 Resume vs Job Description Analyzer")

resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_description = st.text_area("Paste Job Description Here")

if st.button("Analyze"):
    if resume_file and job_description:
        score, matched, missing = analyze_resume(resume_file, job_description)
        st.success(f"✅ Match Score: {score:.2f}%")
        st.markdown("### ✅ Matched Keywords")
        st.write(matched)
        st.markdown("### ❌ Missing Keywords")
        st.write(missing)
    else:
        st.error("Please upload a resume and paste a job description.")
