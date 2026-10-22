import asyncio
import uuid
from datetime import datetime

# Asali Agents ko import kar rahe hain
from agents.crawler_agent import CrawlerAgent
from agents.security_agent import SecurityAgent
from agents.vision_agent import VisionAgent
from agents.reporter_agent import ReporterAgent

class AutoAuditOrchestrator:
    def __init__(self, target_url: str, websocket_manager=None):
        self.target_url = target_url
        self.scan_id = str(uuid.uuid4())
        self.websocket_manager = websocket_manager
        
        self.state = {
            "urls_found": [],
            "security_findings": [],
            "vision_findings": "",
            "report_file": "",
            "status": "Initializing"
        }

    async def send_log(self, agent: str, status: str, message: str):
        if self.websocket_manager:
            log_entry = {
                "agent": agent,
                "status": status,
                "message": message,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            await self.websocket_manager.broadcast(log_entry)
        print(f"[{agent}] {message}")

    async def run_audit(self):
        await self.send_log("System", "info", f"Starting LIVE audit for {self.target_url}")
        
        # --- Step 1: CRAWLER AGENT ---
        crawler = CrawlerAgent(self.target_url)
        found_links = await crawler.crawl(send_log=self.send_log)
        self.state["urls_found"] = found_links

        # --- Step 2: SECURITY & VISION AGENTS (PARALLEL EXECUTION) ---
        await self.send_log("System", "info", "Triggering Security and Vision agents concurrently...")
        
        security_agent = SecurityAgent()
        vision_agent = VisionAgent()

        results = await asyncio.gather(
            security_agent.scan_url(self.target_url, send_log=self.send_log),
            vision_agent.scan_ui(self.target_url, send_log=self.send_log)
        )

        self.state["security_findings"] = results[0]
        self.state["vision_findings"] = results[1]

        # --- Step 3: CRITIC & FINAL REPORT ---
        await self.send_log("Critic", "active", "Filtering data and finalizing state memory...")
        await asyncio.sleep(1) 
        
        # Reporter agent trigger karna
        reporter = ReporterAgent()
        report_filename = await reporter.generate_report(self.target_url, self.scan_id, self.state, self.send_log)
        
        self.state["report_file"] = report_filename
        self.state["status"] = "Completed"
        
        # WebSocket UI ko report ka naam bhejenge
        if self.websocket_manager:
            await self.websocket_manager.broadcast({
                "agent": "System", 
                "status": "completed", 
                "message": "DONE",
                "report_id": report_filename
            })
            
        return self.state