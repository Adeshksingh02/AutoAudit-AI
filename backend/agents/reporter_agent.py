import os
from .base_agent import BaseAgent

class ReporterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Reporter",
            role_prompt="""You are a Chief Information Security Officer (CISO) and expert technical writer. 
            Your job is to take raw JSON data from various security and UI agents and write a professional, 
            well-structured Markdown Executive Summary. 
            Include:
            1. An Executive Overview.
            2. Security Findings (Categorized by severity).
            3. UI/UX Vision Findings.
            4. Actionable Remediation Steps.
            Keep it strictly professional and highly readable. Do not output JSON."""
        )

    async def generate_report(self, target_url: str, scan_id: str, state_data: dict, send_log=None):
        if send_log:
            await send_log("Reporter", "active", "Synthesizing raw data into Executive Summary...")

        # Output folder check & create
        output_dir = os.path.join(os.getcwd(), "outputs")
        os.makedirs(output_dir, exist_ok=True)

        # Gemini ko raw data bhejna format karne ke liye
        prompt = f"""
        Target URL: {target_url}
        Raw Data from Agents:
        - Crawled URLs: {len(state_data.get('urls_found', []))} endpoints
        - Security Findings: {state_data.get('security_findings', [])}
        - Vision UI Findings: {state_data.get('vision_findings', 'None')}

        Write a detailed Markdown report. Make it human-readable.
        """

        try:
            print(f"[{self.name}] Generating Markdown Report...")
            report_content = await self.think_and_act(prompt)
            
            # File save karna
            file_name = f"Audit_Report_{scan_id}.md"
            file_path = os.path.join(output_dir, file_name)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report_content)

            if send_log:
                await send_log("Reporter", "success", f"Report generated successfully: {file_name}")

            return file_name

        except Exception as e:
            error_msg = f"Failed to generate report: {str(e)}"
            if send_log:
                await send_log("Reporter", "error", error_msg)
            return None