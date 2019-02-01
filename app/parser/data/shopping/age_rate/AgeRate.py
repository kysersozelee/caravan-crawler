from dataclasses import dataclass


@dataclass(frozen=True)
class AgeRate:
    code: str
    label: str
    ratio: float

    @staticmethod
    def parse(data_list: list) -> list:
        return list(map(lambda data: AgeRate(data['code'], data['label'], data['ratio']), data_list))
