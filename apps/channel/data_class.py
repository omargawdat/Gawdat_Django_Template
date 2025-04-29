from dataclasses import dataclass
from typing import Literal


@dataclass
class DeviceData:
    registration_id: str
    device_id: str
    type: Literal["android", "ios", "web"]
