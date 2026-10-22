from playwright.async_api import async_playwright
import urllib.parse

class CrawlerAgent:
    def __init__(self, start_url: str):
        self.start_url = start_url
        self.links_found = set()

    async def crawl(self, send_log=None):
        """Website par visit karke saare links aur forms nikalega."""
        if send_log:
            await send_log("Crawler", "active", f"Launching headless browser for {self.start_url}...")
        
        async with async_playwright() as p:
            # Headless browser open kar rahe hain
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                if send_log:
                    await send_log("Crawler", "info", "Extracting DOM and mapping internal links...")
                
                await page.goto(self.start_url, timeout=15000)
                
                # Javascript execute karke saare 'a' tags (links) nikalna
                links = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('a')).map(a => a.href);
                }''')
                
                for link in links:
                    # Sirf valid HTTP/HTTPS links ko filter karenge
                    if link.startswith('http'):
                        self.links_found.add(link)
                
                if send_log:
                    await send_log("Crawler", "success", f"Successfully mapped {len(self.links_found)} links on the target.")
                    
            except Exception as e:
                error_msg = f"Failed to crawl {self.start_url}: {str(e)}"
                if send_log:
                    await send_log("Crawler", "error", error_msg)
                else:
                    print(f"[Crawler Error] {error_msg}")
            finally:
                await browser.close()
                
        return list(self.links_found)