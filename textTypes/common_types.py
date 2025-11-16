from dataclasses import dataclass

@dataclass
class CommonTypes:
    free: str = "free"
    structurized: str = "structurized"
    copy: str = "copy"
    idea: str = "idea"

types = CommonTypes()