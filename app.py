import streamlit as st
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from fpdf import FPDF
import unicodedata

# Clean special characters for PDF compatibility
def clean_text(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

# Filter out short or irrelevant articles
def is_valid_article(text):
    if len(text) < 200:
        return False
    if "copyright" in text.lower() or "all rights reserved" in text.lower():
        return False
    return True

# Load the summarisation model once
@st.cache_resource
def load_summariser():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summariser = load_summariser()

# Search for relevant links using DuckDuckGo
def search_web(topic, max_results=3):
    results = []
    with DDGS() as ddgs:
        for result in ddgs.text(topic, region="wt-wt", safesearch="Moderate", max_results=max_results):
            results.append(result['href'])
    return results

# Fetch article content from a URL
def fetch_article(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join(p.text for p in paragraphs)
        return text[:2000]
    except:
        return ""

# Summarise the text using Hugging Face model
def summarise_text(text):
    result = summariser(text[:1024], max_length=130, min_length=30, do_sample=False)
    return result[0]['summary_text']

# Save the summaries as a PDF
def save_as_pdf(topic, summaries):
    filename = topic.replace(" ", "_") + "_summary.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    topic_clean = clean_text(topic)
    pdf.multi_cell(0, 10, f"Topic: {topic_clean}\n\n")

    for i, summary in enumerate(summaries, 1):
        summary_clean = clean_text(summary)
        pdf.set_font("Arial", "B", size=12)
        pdf.multi_cell(0, 10, f"--- Article {i} ---")
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, summary_clean + "\n")

    pdf.output(filename)
    return filename

# Streamlit App Interface
st.title("Smart Research Assistant")
st.write("Enter a topic and get AI-generated summaries of recent articles.")

topic = st.text_input("Enter a topic to research")

if st.button("Run Research Agent") and topic:
    with st.spinner("Searching and summarising..."):
        urls = search_web(topic)
        summaries = []
        for url in urls:
            st.write(f"Reading: {url}")
            article = fetch_article(url)
            if is_valid_article(article):
                summary = summarise_text(article)
                summaries.append(summary)
            else:
                st.warning("Skipped an article: content was too short or not relevant.")

        for i, summary in enumerate(summaries, 1):
            st.subheader(f"Summary {i}")
            st.write(summary)

        if summaries:
            pdf_file = save_as_pdf(topic, summaries)
            with open(pdf_file, "rb") as f:
                st.download_button("Download PDF Summary", f, file_name=pdf_file)

    st.success("Research completed.")
