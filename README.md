# caravan-crawler
[네이버 데이터랩](https://datalab.naver.com/shoppingInsight/sCategory.naver) 크롤링 프로젝트

## development environment
- pyenv
- python 3.7.0

## virtual env settings
```bash
# activate venv
$ python3 -m venv ./venv
$ source ./venv/bin/activate

# install requirements
$ pip3 install -r requirements.txt

# deactivate
$ deactivate
```

## test
##### console
```bash
$ pytest ./test
```

##### intellij
```text
Edit Configurations -> Python tests -> Add New Configuration('+') click
  -> Python tests -> py.test -> 'Target setting' with 'Script path' -> select path -> run
``` 

## ETC
- code style : [PEP8](https://www.python.org/dev/peps/pep-0008)
