import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Step 2: Preprocess text (tokenize + clean)
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in tokens if word.isalpha() and word not in stop_words]
    return set(keywords)

# Step 3: Compare keywords
def compare_keywords(resume_keywords, job_keywords):
    common = resume_keywords & job_keywords
    missing = job_keywords - resume_keywords
    match_percent = (len(common) / len(job_keywords)) * 100 if job_keywords else 0
    return match_percent, common, missing

# Step 4: Main
if __name__ == "__main__":
    resume_path = input("Enter resume PDF path: ")
    job_description = input("Paste job description: ")

    resume_text = extract_text_from_pdf(resume_path)
    job_text = job_description

    resume_keywords = preprocess_text(resume_text)
    job_keywords = preprocess_text(job_text)

    score, matched, missing = compare_keywords(resume_keywords, job_keywords)

    print(f"\n📝 Match Score: {score:.2f}%")
    print(f"✅ Matched Keywords: {list(matched)}")
    print(f"❌ Missing Keywords: {list(missing)}")
