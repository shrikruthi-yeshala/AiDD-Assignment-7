"""
Screenshot generator for project detail pages.
This script captures screenshots of each project detail page and saves them.
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Project slugs to screenshot
PROJECTS = {
    "employee-productivity": "teams-app-screenshot.jpg",
    "servicenow-ai": "servicenow-ai-screenshot.jpg",
    "powerbi-dashboard": "powerbi-dashboard-screenshot.jpg",
    "sap-enterprise": "sap-gui-screenshot.jpg",
}

BASE_URL = "http://127.0.0.1:5000"
IMAGES_DIR = Path(__file__).parent / "static" / "images"


def capture_screenshots():
    """Capture screenshots of all project detail pages."""
    print("Starting screenshot capture process...")
    print(f"Saving to: {IMAGES_DIR}")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            device_scale_factor=1
        )
        page = context.new_page()
        
        for slug, filename in PROJECTS.items():
            url = f"{BASE_URL}/projects/docs/{slug}"
            output_path = IMAGES_DIR / filename
            
            try:
                print(f"\n📸 Capturing: {slug}")
                print(f"   URL: {url}")
                
                # Navigate to page
                page.goto(url, wait_until="networkidle", timeout=10000)
                
                # Wait a bit for any animations/rendering
                time.sleep(1)
                
                # Take screenshot
                page.screenshot(path=str(output_path), full_page=False)
                
                print(f"   ✅ Saved: {filename}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        browser.close()
    
    print("\n✨ Screenshot capture complete!")


if __name__ == "__main__":
    # Check if Flask server is running
    import requests
    try:
        response = requests.get(BASE_URL, timeout=2)
        if response.status_code:
            print("✅ Flask server is running")
            capture_screenshots()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Flask server is not running!")
        print("Please start the server first: python app.py")
