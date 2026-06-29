import json
import os
import shutil
from playwright.sync_api import sync_playwright

def run():
    # Setup a temporary clean profile directory for the session
    user_data_dir = os.path.join(os.getcwd(), "playwright_profile")
    
    with sync_playwright() as p:
        print("Launching stealth browser context...")
        
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,  # Set to True later if you want it completely hidden
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            ignore_default_args=["--enable-automation"],
            viewport=None
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        captured_data = {"found": False}

        # Background API Interceptor
        def handle_response(response):
            # FIXED: Changed response.status_code to response.status
            if "getMatchList" in response.url and response.status == 200:
                try:
                    data = response.json()
                    with open("match_list.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    print("\n🎉 Success! Captured data and saved to match_list.json")
                    captured_data["found"] = True
                except Exception as e:
                    print(f"Found URL but couldn't parse JSON: {e}")

        page.on("response", handle_response)

        print("Navigating to Oddspedia...")
        page.goto("https://oddspedia.com/ca/baseball/usa/mlb/odds", wait_until="commit")

        print("Waiting for page load and API payload...")
        # Keep monitoring until data is captured or 15 seconds pass
        for _ in range(15):
            if captured_data["found"]:
                break
            page.wait_for_timeout(3000)

        if not captured_data["found"]:
            print("❌ Failed to capture the API. Try interacting with or scrolling the page.")
        
        context.close()

    # Clean up the temporary profile folder
    if os.path.exists(user_data_dir):
        shutil.rmtree(user_data_dir)

if __name__ == "__main__":
    run()