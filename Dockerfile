FROM python:3.7.2-alpine3.9

MAINTAINER Austin Michne "austinmichne@gmail.com" 
EXPOSE 80

COPY . .
# WORKDIR .

RUN apk add gcc libc-dev linux-headers mariadb-dev

RUN pip install -r requirements.txt

CMD python ./server.py --user "" --password "" --host "" --db "derived"