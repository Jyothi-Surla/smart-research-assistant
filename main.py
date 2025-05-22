from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from fpdf import FPDF

# Load the Hugging Face summarisation model
summariser = pipeline("summarization", model="facebook/bart-large-cnn")

def search_web(topic, max_results=3):
    results = []
    with DDGS() as ddgs:
        for result in ddgs.text(topic, region="wt-wt", safesearch="Moderate", max_results=max_results):
            results.append(result['href'])
    return results

def fetch_article(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join(p.text for p in paragraphs)
        return text[:2000]  # Limit for summarisation
    except:
        return ""

def summarise_text(text):
    print("🤖 Summarising with Hugging Face...")
    result = summariser(text[:1024], max_length=130, min_length=30, do_sample=False)
    return result[0]['summary_text']

def save_summary(topic, summaries):
    filename = topic.replace(" ", "_") + "_summary.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Topic: {topic}\n\n")
        for i, summary in enumerate(summaries, 1):
            f.write(f"\n--- Article {i} ---\n")
            f.write(summary)
            f.write("\n")
    print(f"\n✅ Text summary saved to {filename}")

def save_as_pdf(topic, summaries):
    filename = topic.replace(" ", "_") + "_summary.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, f"Topic: {topic}\n\n")

    for i, summary in enumerate(summaries, 1):
        pdf.set_font("Arial", "B", size=12)
        pdf.multi_cell(0, 10, f"--- Article {i} ---")
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, summary + "\n")

    pdf.output(filename)
    print(f"✅ PDF summary saved to {filename}")

def run_agent():
    topic = input("Enter a topic to research: ")
    print("🔍 Searching...")
    urls = search_web(topic)

    summaries = []
    for url in urls:
        print(f"📖 Reading: {url}")
        article = fetch_article(url)
        if article:
            summary = summarise_text(article)
            summaries.append(summary)

    save_summary(topic, summaries)
    save_as_pdf(topic, summaries)

if __name__ == "__main__":
    run_agent()
