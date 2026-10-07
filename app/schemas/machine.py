from pydantic import BaseModel


class MachineBase(BaseModel):
    code: str
    name: str
    type: str
    line: str
    status: str
    capacity_per_hour: float
    active: bool = True


class MachineCreate(MachineBase):
    pass


class MachineUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    type: str | None = None
    line: str | None = None
    status: str | None = None
    capacity_per_hour: float | None = None
    active: bool | None = None


class Machine(MachineBase):
    id: int
