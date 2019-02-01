from dataclasses import dataclass

from main.parser.data.rank.RankReponse import RankResponse


@dataclass(frozen=True)
class KeywordRank:
    rank: int
    keyword: str
    linkId: str

    @staticmethod
    def parse(rank_response: RankResponse) -> list:
        rank_list = rank_response.ranks

        return list(
            map(lambda rank: KeywordRank(rank['rank'], rank['keyword'], rank['linkId']), rank_list))
