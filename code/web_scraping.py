import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display

URL = "https://www.cnbc.com/world/?region=world"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

OUTPUT_PATH = "web_data.html"

def fetch_page_html(url: str) -> str | None:
    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(f"user-agent={HEADERS['User-Agent']}")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print(f"Fetching URL: {url}")
        driver.get(url)

        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        import time

        # wait for page load
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # scroll to trigger lazy loading
        for _ in range(6):
            driver.execute_script("window.scrollBy(0, 900);")
            time.sleep(1)

        print("Page title:", driver.title)
        print("HTML length:", len(driver.page_source))

        return driver.page_source

    except Exception as e:
        print("Selenium error:", e)
        return None

    finally:
        if driver:
            driver.quit()
def save_html(html: str) -> None:
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML saved to {OUTPUT_PATH}")


def main():
    html = fetch_page_html(URL)

    if html:
        save_html(html)
    else:
        print("HTML could not be retrieved")


if __name__ == "__main__":
    main()
