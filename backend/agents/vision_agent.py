import io
import PIL.Image
from playwright.async_api import async_playwright
from .base_agent import BaseAgent

class VisionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Vision",
            role_prompt="""You are an elite UI/UX and Visual QA Auditor. 
            Analyze the provided website screenshot. Point out any visible UI bugs, 
            overlapping text, low-contrast issues, or broken layouts. 
            Be concise and professional. Categorize findings into 'Visual Bug' or 'UX Improvement'."""
        )

    async def scan_ui(self, url: str, send_log=None):
        if send_log:
            await send_log("Vision", "active", f"Launching headless browser to capture UI of {url}...")
        
        try:
            # 1. Playwright se Screenshot lena
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=15000)
                
                if send_log:
                    await send_log("Vision", "info", "Snapping high-resolution screenshot...")
                
                # Screenshot ko bytes me memory me save karna (fast execution ke liye)
                screenshot_bytes = await page.screenshot(full_page=False)
                await browser.close()

            # 2. Bytes ko Image object me convert karna Gemini ke liye
            image = PIL.Image.open(io.BytesIO(screenshot_bytes))

            if send_log:
                await send_log("Vision", "active", "Sending screenshot to Gemini Vision for UI/UX audit...")

            # 3. Gemini Vision API Call
            prompt = f"Analyze this screenshot of {url}. Point out any visual flaws or UX issues."
            
            print(f"[{self.name}] Analyzing Image...")
            # Gemini ko text aur image ek sath bhej rahe hain
            response = self.model.generate_content([prompt, image])
            
            if send_log:
                await send_log("Vision", "success", "Visual UI audit completed successfully.")

            return response.text

        except Exception as e:
            error_msg = f"Vision scan failed: {str(e)}"
            if send_log:
                await send_log("Vision", "error", error_msg)
            return error_msg