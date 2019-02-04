# caravan-crawler
[네이버 데이터랩](https://datalab.naver.com/shoppingInsight/sCategory.naver) 크롤링 프로젝트

## Development environment
- pyenv
- python 3.7.0
- docker

## Virtual env settings
```bash
# activate venv
$ python3 -m venv ./venv
$ source ./venv/bin/activate

# install requirements
$ pip3 install -r requirements.txt

# deactivate
$ deactivate
```

## Test
##### console
```bash
$ pytest -v ./test
```

##### intellij
```text
Edit Configurations -> Python tests -> Add New Configuration('+') click
  -> Python tests -> py.test -> 'Target setting' with 'Script path' -> select path -> run
``` 

## DB
```bash
# install mysql connector first
$ brew install mysql-connector-c

# docker
docker run --name caravan-mysql \
-p 3308:3306 -v $WORKSPACE/git/caravan/caravan-mysql:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=caravan -e MYSQL_USER=caravan \
-e MYSQL_PASSWORD=caravan -e MYSQL_DATABASE=caravan -d \
-e TZ=Asia/Seoul \
mysql:8.0.14 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

## ETC
- code style : [PEP8](https://www.python.org/dev/peps/pep-0008)
