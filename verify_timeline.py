from playwright.sync_api import sync_playwright, expect
import time
import os

def test_timeline(page):
    print("Navigating to timeline...")
    page.goto("http://127.0.0.1:5000/")

    # Wait for loading to finish
    print("Waiting for loading...")
    expect(page.locator("text=Loading...")).not_to_be_visible(timeout=10000)

    # Check for presence of spell icons or text
    print("Checking for spells...")
    # "Fight or Flight" is a Paladin spell. Default spec is Red Mage though.
    # Default spec in timelinev2.html is `const [selectedSpec, setSelectedSpec] = useState('redmage-redmage');`
    # Red Mage spells: "Embolden", "Fleche", "Contre Sixte"

    expect(page.get_by_title("Embolden")).to_be_visible()

    # Check if a specific element from spell_data.json is rendered
    # We can check network requests to confirm it fetched spell_data.json?
    # Playwright can intercept network requests.

    print("Taking screenshot...")
    os.makedirs("/home/jules/verification", exist_ok=True)
    page.screenshot(path="/home/jules/verification/timeline_v2.png")
    print("Screenshot saved.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Monitor network requests
        page.on("request", lambda request: print(f"Request: {request.url}"))

        try:
            test_timeline(page)
        except Exception as e:
            print(f"Test failed: {e}")
            page.screenshot(path="/home/jules/verification/error.png")
        finally:
            browser.close()
