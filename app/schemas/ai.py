from pydantic import BaseModel


class ProductionStatistics(BaseModel):
    total_production: int
    total_scrap: int
    scrap_rate: float


class MachinePerformance(BaseModel):
    machine: str
    machine_name: str
    total_production: int
    total_scrap: int
    scrap_rate: float


class ProductionAnalysisResponse(BaseModel):
    model: str
    statistics: ProductionStatistics
    machines: list[MachinePerformance]
    highest_scrap_machine: MachinePerformance | None
    analysis: str
