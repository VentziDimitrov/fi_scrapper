import os
from playwright.sync_api import sync_playwright
from ai_agent import AIAgent
from vector_db_manager import VectorDBManager

# ========== CONFIG ==========
BASE_URL = "https://www.fibank.bg/bg/chastni-lica/karti"
OUTPUT_DIR = "fibank_chunks"
# ============================

def scrape_fi_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)
        page.wait_for_selector(".accounts-list")
        locator = page.locator(".accounts-list")
        html_raw = locator.inner_html()
        browser.close()
        return html_raw
    
def write_to_file(filename: str, content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fname = os.path.join(OUTPUT_DIR, filename)
    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    
    
raw_content = scrape_fi_page()

agent = AIAgent()
data = agent.parse_html(raw_content)

write_to_file("chunks.md", data)

#print("Done!")

""" #Prepare for inserting into vector DB
dbManager = VectorDBManager()
dbManager.embed_items(data) """