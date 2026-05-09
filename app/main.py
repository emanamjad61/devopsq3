from fastapi import FastAPI, Query
import uvicorn
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = FastAPI()
REGISTRATION_ID = "STUDENT_XYZ_2026"

def get_selenium_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1365,1000")
    # Anti-bot flags
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def summarize_text(text):
    if not text or len(text) < 20: return "No content available."
    sentences = text.split(".")
    return ". ".join(sentences[:3]).strip()

def scrape_pakistan_today(keyword):
    driver = get_selenium_driver()
    try:
        # Step 1: Human-like access to landing page
        driver.get("https://www.pakistantoday.com.pk/")
        time.sleep(random.uniform(5, 8))
        
        # Step 2: Access search directly
        driver.get(f"https://www.pakistantoday.com.pk/?s={keyword}")
        time.sleep(random.uniform(3, 5))
        
        # Step 3: Extract results
        results = driver.find_elements(By.CSS_SELECTOR, "h3.entry-title a, .td-module-title a")
        
        if not results:
             # Fallback: if we can't see results, check if blocked
             title = driver.title
             if "Just a moment" in title or "Cloudflare" in title:
                 return {"error": "Cloudflare challenge presented. Please try again in a moment."}
             return {"error": f"No results found for keyword: {keyword}"}

        first_article = results[0]
        article_url = first_article.get_attribute("href")
        article_snippet = first_article.text # Fallback summary from title/snippet

        # Step 4: Try to get full content
        try:
            driver.get(article_url)
            time.sleep(random.uniform(3, 4))
            paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p, .td-post-content p")
            article_text = "\n".join([p.text for p in paragraphs if len(p.text.strip()) > 20])
            summary = summarize_text(article_text) if article_text else article_snippet
        except:
            summary = article_snippet # Use the search result title as summary if blocked on article page

        return {
            "registration": REGISTRATION_ID,
            "newssource": "Pakistan Today",
            "keyword": keyword,
            "url": article_url,
            "summary": summary
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()

@app.get("/get")
async def get_article(keyword: str):
    return scrape_pakistan_today(keyword)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
