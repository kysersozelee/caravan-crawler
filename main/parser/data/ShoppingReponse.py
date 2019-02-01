from dataclasses import dataclass

from main.parser.data.ShoppingParam import ShoppingParam


@dataclass(frozen=True)
class ShoppingResponse:
    code: str
    message: str
    shopping_param: ShoppingParam
    chart_type: str
    range: str
    result: list
    success: bool

    @staticmethod
    def parse(response: dict):
        shopping_param = ShoppingParam.parse(response['shoppingParam'])

        return ShoppingResponse(response['code'],
                                response['message'],
                                shopping_param,
                                response['chartType'],
                                response['range'],
                                response['result'],
                                response['success']
                                )
