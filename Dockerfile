FROM python:latest
ENV PYTHONUNBUFFERED=1
ENV TZ Asia/Seoul
RUN apt-get update \
    && apt-get install -y --no-install-recommends default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["ls", "-alF"]
CMD ["python", "actProjects/manage.py", "runserver", "0.0.0.0:8000"]
