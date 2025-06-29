from playwright.sync_api import sync_playwright
import re

def get_latest_multipliers(limit=50):
    url = "https://www.premierbet.com/tg/casino/game/aviator-2007"
    multipliers = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)
        content = page.content()
        browser.close()
    matches = re.findall(r"(\d+\.\d+)x", content)
    for m in matches[-limit:]:
        multipliers.append(float(m))
    return multipliers