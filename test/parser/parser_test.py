import json
import os

from main.parser.Parser import Parser
from main.parser.data.AgeRate import AgeRate
from main.parser.data.ShoppingReponse import ShoppingResponse


# TODO : test data 읽어 올 때 상대경로 제거
def test_response_data_class():
    with open('%s/../resources/age_rate_sample.txt' % os.path.dirname(os.path.abspath(__file__))) as f:
        response = ShoppingResponse.parse(json.loads(f.readlines()[0]))
        assert response.chart_type == 'barChart'
        assert response.code == ''
        assert response.message == ''
        assert response.range == '2017.08.01. ~ 2019.02.01.'
        assert response.success is True

        shopping_param = response.shopping_param
        assert shopping_param.age == '10,20,30,40,50,60'
        assert shopping_param.cid == '50001768'
        assert shopping_param.count == 0
        assert shopping_param.date is None
        assert shopping_param.dateRange == '2017.08.01. ~ 2019.02.01.'
        assert shopping_param.device == 'pc,mo'
        assert shopping_param.end_date == '2019-02-01'
        assert shopping_param.gender == 'f,m'
        assert shopping_param.keyword is None
        assert shopping_param.page == 0
        assert shopping_param.start_date == '2017-08-01'
        assert shopping_param.time_unit == 'date'
        assert shopping_param.type is None


def test_age_rate_parsing(mocker):
    with open('%s/../resources/age_rate_sample.txt' % os.path.dirname(os.path.abspath(__file__))) as f:
        mocker.patch.object(Parser, 'datalab_api_call')
        Parser.datalab_api_call.return_value = json.loads(f.readlines()[0])
        params = Parser.get_params("50001768", "2019-02-01")
        age_rate_list = Parser.get_age_rate(params)

        assert len(age_rate_list) == 1
        age_rate: AgeRate = age_rate_list[0]
        assert len(age_rate.data) == 6
        assert age_rate.code is None
        assert age_rate.full_title is None
        assert age_rate.title == '50001768'
