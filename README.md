# RaonAir(likeLion_ideathon)

멋쟁이 사자처럼 9기 아이디어톤 라온에어(ActLike)

## Requirements

- python3

## How to run server

- 가상환경 생성

```shell
python -m venv raon_venv  # myvenv는 자신이 원하는 가상환경 이름으로 교체해도 무방
```

- 가상환경 실행

```shell
source raon_venv/Scripts/activate  # Windows
source raon_venv/bin/activate  # macOS
```

- 의존 패키지 설치

```shell
pip install -r requirements.txt
```

- 프로젝트 시작 (사용하는 데는 필요없음)

```shell
django-admin startproject actProjects
cd actProjects
```

- 서버 실행

```shell
python manage.py runserver

python actProjects/manage.py runserver
```

## After inspectdb command (important!)

- Django의 inpectdb 명령어가 default 속성을 제대로 가져오지 못하는 문제가 있어, inspectdb 명령어 이후에는 아래의 커맨드를 반드시 실행해야 한다.

```shell
python after-inspectdb.py
```
