from playwright.sync_api import sync_playwright

def handle_response(response):
    if "getMatchList" in response.url:
        print(response.json())

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.on("response", handle_response)

    page.goto("https://oddspedia.com/ca/baseball/usa/mlb/odds")

    page.wait_for_timeout(5000)