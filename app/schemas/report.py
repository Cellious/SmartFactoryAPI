from pydantic import BaseModel


class MachinePerformanceReport(BaseModel):
    machine: str
    machine_name: str
    total_production: float
    total_scrap: float
    scrap_rate: float
