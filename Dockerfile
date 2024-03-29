FROM python:3.9-alpine3.12

RUN mkdir /holiday_api
COPY . /holiday_api
WORKDIR /holiday_api

RUN pip install -r requirements.txt &&\
	pip install -e . &&\
	rm -rfv /var/cache/apk/*;

WORKDIR /holiday_api/holiday_api

CMD ["uvicorn", "--host", "0.0.0.0",\
	"--proxy-headers", "--forwarded-allow-ips=*",\
	"main:app", "--reload"]