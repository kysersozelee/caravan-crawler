from dataclasses import dataclass


@dataclass(frozen=True)
class RankResponse:
    message: str
    status_code: int
    return_code: int
    date: str
    datatime: str
    range: str
    ranks: list

    @staticmethod
    def parse(response: dict):
        return RankResponse(response['message'],
                            response['statusCode'],
                            response['returnCode'],
                            response['date'],
                            response['datetime'],
                            response['range'],
                            response['ranks']
                            )
