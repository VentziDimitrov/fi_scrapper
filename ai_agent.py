import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

# ========== CONFIG ==========
MODEL = "gpt-4o-mini"  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AIAgent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = MODEL
        
    def parse_html(self, html: str) -> dict:
        prompt = f""" 
You are an expert HTML parsing agent specialized in extracting structured data from HTML content. Your task is to parse HTML code containing product/service listings and extract specific information from each list item.

## Your Mission
Parse the provided HTML code and extract the following information from each `accounts-list__item`:

1. **URL** - Convert relative href to absolute URL with root: `https://www.fibank.bg/`
2. **Title** - Extract title from current element
3. **Description** - Extract description from current element

## Output Format
Return your results as a JSON array where each object follows this exact structure:
{{
  "url": "string",
  "title": "string", 
  "description": "string"
}}

## Parsing Rules
- **URL Construction**: Take the `href` attribute from the `<a>` tag and prepend `https://www.fibank.bg/` to create the absolute URL
- **Title Extraction**: Get the text content`
- **Description Extraction**: Get the decription
- **Text Cleaning**: Trim whitespace and preserve line breaks where they exist naturally in the HTML
- **Multiple Items**: Process all list item elements (div's) found in the HTML

## Expected HTML Structure
<div class="accounts-list__item">
  <div class="accounts-list__inner">
    <a href="/relative/path/here">
      <div class="accounts-list__preview">
        <img src="..." alt="...">
      </div>
      <div class="accounts-list__text">
        <h3 class="accounts-list__title">Product Title</h3>
        <p>Product description text...</p>
      </div>
    </a>
  </div>
</div>

## Important Notes
- Handle both single and multiple list items
- Preserve original language/characters (including Cyrillic text)
- Return valid JSON format only
- If any required field is missing, use empty string as value
- Process items in the order they appear in the HTML

## Example Input/Output
**Input HTML:**
<div class="accounts-list__item">
  <div class="accounts-list__inner">
    <a href="/bg/chastni-lica/karti/virtualna-kreditna-karta">
      <div class="accounts-list__text">
        <h3 class="accounts-list__title">Виртуална кредитна карта</h3>
        <p>Издай на секундата!</p>
      </div>
    </a>
  </div>
</div>


**Expected Output:**
[
  {{
    "url": "https://www.fibank.bg/bg/chastni-lica/karti/virtualna-kreditna-karta",
    "title": "Виртуална кредитна карта",
    "description": "Издай на секундата!"
  }}
]


Now process the HTML code that will be provided to you and return the extracted data in the specified JSON format. 
Here the code: {html} 
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        def strip_code_fences(text: str) -> str:
            return text.replace("```json", "").replace("```", "").strip()
        
        #print("AI JSON Output:", json_output)
        try:
            json_output = response.choices[0].message.content.strip()
            stripped =  strip_code_fences(json_output)
            return stripped
        except Exception:
            raise ValueError(f"Failed to parse AI output as JSON")
        
   
