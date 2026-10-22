import httpx
from .base_agent import BaseAgent

class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Security",
            role_prompt="""You are an elite Cybersecurity Penetration Tester. 
            Analyze the provided HTTP headers and HTML snippets to identify security vulnerabilities.
            Look for exposed API keys, missing security headers, XSS vectors, and bad practices.
            Keep your analysis concise and mention the severity (CRITICAL, HIGH, MEDIUM, LOW)."""
        )

    async def scan_url(self, url: str, send_log=None):
        findings = []
        if send_log:
            await send_log("Security", "active", f"Initiating security scan on {url}...")
            
        try:
            # Asynchronously website ka data fetch karna (taaki server block na ho)
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                headers = response.headers
                html_body = response.text
                
                # 1. Standard Rule-Based Checks (Speed ke liye)
                if 'x-frame-options' not in headers:
                    findings.append({"severity": "Medium", "issue": "Missing X-Frame-Options (Clickjacking risk)"})
                if 'strict-transport-security' not in headers:
                    findings.append({"severity": "Medium", "issue": "Missing HSTS Header"})
                
                if send_log:
                    await send_log("Security", "info", f"Completed rule-based header checks. Found {len(findings)} issues.")
                
                # 2. AI Reasoning (Smart Scanning)
                if send_log:
                    await send_log("Security", "active", "Sending HTML snippet to Gemini for advanced logic flaw detection...")
                
                # Token limit se bachne ke liye sirf shuruwaati 3000 characters bhej rahe hain
                snippet = html_body[:3000]
                prompt_data = f"Target URL: {url}\nHeaders: {dict(headers)}\nHTML Snippet: {snippet}\nAre there any obvious security misconfigurations or exposed secrets here?"
                
                ai_analysis = await self.think_and_act(prompt_data)
                findings.append({"severity": "AI-Insight", "issue": "LLM Analysis Result", "details": ai_analysis})
                
                if send_log:
                    await send_log("Security", "success", "AI Security analysis completed.")
                    
        except Exception as e:
            if send_log:
                await send_log("Security", "error", f"Scan failed for {url}: {str(e)}")
                
        return findings