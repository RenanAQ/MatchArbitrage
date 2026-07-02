import json
import os
import shutil
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth


def get_page_two_odds():
    # The signature endpoint we want to catch in the background traffic
    target_endpoint = "getAmericanMaxOddsWithPagination"

    # Container to hold our captured JSON data
    captured_data = {"json": None}

    user_data_dir = os.path.join(os.getcwd(), "playwright_profile")
    if os.path.exists(user_data_dir):
        shutil.rmtree(user_data_dir)

    with Stealth().use_sync(sync_playwright()) as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,  # Keep False to allow Cloudflare to resolve naturally
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ],
        )

        page = context.pages[0] if context.pages else context.new_page()

        # Define the network inspector callback function
        def intercept_response(response):
            if target_endpoint in response.url:
                try:
                    # Capture the clean JSON directly from the browser's internal network state
                    captured_data["json"] = response.json()
                    print(
                        f"[Network Intercept] Successfully captured API Data from: {response.url[:60]}..."
                    )
                except Exception:
                    pass

        # Attach the network listener to the page
        page.on("response", intercept_response)

        print("Navigating to Oddspedia...")
        page.goto(
            "https://oddspedia.com/ca/baseball/usa/mlb/odds",
            wait_until="domcontentloaded",
        )

        print(
            "Waiting for the page to naturally query the API and pass Cloudflare..."
        )

        # Loop and wait for the target network response to be filled
        for _ in range(15):
            page.wait_for_timeout(1000)
            if captured_data["json"] is not None:
                break

        context.close()
        if os.path.exists(user_data_dir):
            shutil.rmtree(user_data_dir)

        if captured_data["json"] is None:
            raise Exception(
                "Could not intercept the API call. Cloudflare challenge may have blocked it."
            )

        return captured_data["json"]


if __name__ == "__main__":
    try:
        data = get_page_two_odds()

        with open("wX-odds.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("Success! Data saved to wX-odds.json")

    except Exception as e:
        print(f"Failed to fetch data: {e}")