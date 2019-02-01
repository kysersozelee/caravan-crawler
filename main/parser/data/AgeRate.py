from dataclasses import dataclass

from main.parser.data import ShoppingReponse


@dataclass(frozen=True)
class AgeRate:
    code: str
    title: str
    full_title: str
    data: list

    @staticmethod
    def parse(shopping_response: ShoppingReponse) -> list:
        data_list = shopping_response.result

        return list(map(lambda data: AgeRate(data['code'], data['title'], data['fullTitle'], data['data']), data_list))
