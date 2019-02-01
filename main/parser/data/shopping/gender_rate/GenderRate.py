from dataclasses import dataclass

from main.parser.data.shopping import ShoppingReponse


@dataclass(frozen=True)
class GenderRate:
    code: str
    label: str
    ratio: float

    @staticmethod
    def parse(data_list: list) -> list:
        return list(map(lambda data: GenderRate(data['code'], data['label'], data['ratio']), data_list))
