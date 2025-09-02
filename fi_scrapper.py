import os
import json
from playwright.sync_api import sync_playwright
from ai_agent import AIAgent
from vector_db_manager import VectorDBManager

# ========== CONFIG ==========
BASE_URL = "https://www.fibank.bg/bg/chastni-lica/karti"
OUTPUT_DIR = "fibank_chunks"
# ============================

"""
    Launches a headless Chromium browser, navigates to BASE_URL, and returns the inner HTML
    of an element matching the CSS selector ".accounts-list".

    Steps performed:
    1. Uses a context manager (`with sync_playwright() as p:`) to start and cleanly close Playwright,
       following recommended usage patterns :contentReference[oaicite:1]{index=1}.
    2. Launches a Chromium browser instance.
    3. Opens a new page and navigates to the global `BASE_URL`.
    4. Waits for the element `.accounts-list` to appear in the DOM.
    5. Locates the element and captures its inner HTML.
    6. Closes the browser.
    7. Returns the raw HTML string for further processing.

    Returns:
        str: The HTML content contained within the ".accounts-list" element.
"""

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


"""
    Writes the provided content to a file in the OUTPUT_DIR directory.

    Args:
        filename (str): Name of the file to write to.
        content: The content to write (usually a string).

    The function ensures OUTPUT_DIR exists, then writes the content
    to the specified file using UTF-8 encoding.
"""
def write_to_file(filename: str, content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fname = os.path.join(OUTPUT_DIR, filename)
    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    
    
raw_content = scrape_fi_page()

agent = AIAgent()
data = agent.parse_html(raw_content)

dbManager = VectorDBManager()
items = dbManager.check_chunk_size(data, max_tokens=500)

write_to_file("chunks.md", json.dumps(items, indent=2, ensure_ascii=False))

#print("Done!")

""" #Prepare for inserting into vector DB
dbManager.embed_items(data) 
"""
