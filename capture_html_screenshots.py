"""
Screenshot generator for standalone HTML project pages.
Captures screenshots from the personalsite HTML files.
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# HTML files to screenshot
HTML_FILES = {
    "powerbi-dashboard.html": "powerbi-dashboard-screenshot.jpg",
    "sap-enterprise-documentation.html": "sap-gui-screenshot.jpg",
    "servicenow-ai-documentation.html": "servicenow-ai-screenshot.jpg",
    "servicenow-documentation.html": "servicenow-platform-screenshot.jpg",
    "productivity-sheet.html": "teams-app-screenshot.jpg",
}

SOURCE_DIR = Path("C:/Users/shrikruthi yeshala/Downloads/personalsite")
OUTPUT_DIR = Path(__file__).parent / "static" / "images"


def capture_html_screenshots():
    """Capture screenshots of standalone HTML files."""
    print("Starting screenshot capture from HTML files...")
    print(f"Source: {SOURCE_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            device_scale_factor=1
        )
        page = context.new_page()
        
        for html_file, screenshot_file in HTML_FILES.items():
            html_path = SOURCE_DIR / html_file
            output_path = OUTPUT_DIR / screenshot_file
            
            if not html_path.exists():
                print(f"\n❌ {html_file}: File not found at {html_path}")
                continue
            
            try:
                print(f"\n📸 Capturing: {html_file}")
                print(f"   Source: {html_path}")
                
                # Navigate to local HTML file
                file_url = f"file:///{str(html_path).replace(chr(92), '/')}"
                page.goto(file_url, wait_until="networkidle", timeout=15000)
                
                # Wait for content to render
                time.sleep(2)
                
                # Take screenshot
                page.screenshot(path=str(output_path), full_page=False)
                
                # Get file size
                size_kb = output_path.stat().st_size / 1024
                print(f"   ✅ Saved: {screenshot_file} ({size_kb:.1f} KB)")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        browser.close()
    
    print("\n✨ Screenshot capture complete!")
    print("\nGenerated screenshots:")
    for screenshot_file in HTML_FILES.values():
        output_path = OUTPUT_DIR / screenshot_file
        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"  ✅ {screenshot_file} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    capture_html_screenshots()
