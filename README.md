## Smart Research Assistant

This is a simple AI-powered tool I built that helps you research any topic by searching the web, summarising recent articles using a Hugging Face model, and generating a downloadable PDF summary. It runs entirely in the browser through a Streamlit interface.

---

## What it does

- Takes any topic as input  
- Searches the web using DuckDuckGo  
- Scrapes content from real articles  
- Summarises them using a pre-trained AI model (`facebook/bart-large-cnn`)  
- Creates a clean PDF report that can be downloaded  

---

## Tools and Technologies

- Python  
- Streamlit  
- Hugging Face Transformers  
- DuckDuckGo Search  
- BeautifulSoup (for parsing HTML)  
- FPDF (for creating the PDF)  

---

## How to run it locally

1. ```Clone this repository:
git clone https://github.com/Jyothi-Surla/smart-research-assistant.git
cd smart-research-assistant```

2.``` Install the required packages:
pip install -r requirements.txt```

3. ```Start the app:
streamlit run app.py```
---

## Live App
You can try the app here:  
**https://jyothi-surla-smart-research-assistant.streamlit.app**
