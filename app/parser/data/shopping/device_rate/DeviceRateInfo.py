from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceRateInfo:
    code: str
    title: str
    full_title: str
    device_rate_list: list
