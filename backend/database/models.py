from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Enums for severity levels
class SeverityLevel:
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Vulnerability(BaseModel):
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    agent_name: str
    severity: str
    title: str
    description: str
    url: str
    timestamp: datetime = Field(default_factory=datetime.now)
    remediation: Optional[str] = None

class ScanJob(BaseModel):
    job_id: str
    target_url: str
    status: str = "Running" # Running, Completed, Failed
    discovered_urls: List[str] = []
    vulnerabilities: List[Vulnerability] = []
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None