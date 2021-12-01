FROM python:3.9

RUN apt-get update && apt-get -y install python3 python3-dev python3-pip gcc g++ libffi-dev sqlite3

RUN pip install uvicorn fastapi fastapi_login sqlalchemy \
    pydantic python-dotenv wheel python-multipart python-binance \
    bcrypt pycryptodomex jinja2

#RUN git clone https://github.com/Jimmy-Xu/fastapi-web-starter.git -b mine /fastapi-web-starter
ADD app /fastapi-web-starter/app
ADD images /fastapi-web-starter/images
ADD static /fastapi-web-starter/static
ADD templates /fastapi-web-starter/templates
ADD app.db /fastapi-web-starter/app.db


WORKDIR /fastapi-web-starter

RUN echo -e "ctrKey=\nsecret=\nSECRET=" > .env

EXPOSE 8080

CMD /usr/local/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
