# streamlit_app.py

import streamlit as st
import fitz
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download("punkt")
nltk.download("stopwords")

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english") + list(string.punctuation))
    return set([word for word in tokens if word.isalpha() and word not in stop_words])

def compare_keywords(resume_keywords, job_keywords):
    common = resume_keywords & job_keywords
    missing = job_keywords - resume_keywords
    score = (len(common) / len(job_keywords)) * 100 if job_keywords else 0
    return score, common, missing

st.title("📄 Resume Analyzer")

resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_description = st.text_area("Paste the Job Description")

if st.button("Analyze") and resume_file and job_description:
    resume_text = extract_text_from_pdf(resume_file)
    resume_keywords = preprocess_text(resume_text)
    job_keywords = preprocess_text(job_description)
    score, matched, missing = compare_keywords(resume_keywords, job_keywords)

    st.success(f"Match Score: {score:.2f}%")
    st.markdown("### ✅ Matched Keywords")
    st.write(list(matched))
    st.markdown("### ❌ Missing Keywords")
    st.write(list(missing))
