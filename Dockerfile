FROM ubuntu:18.04
MAINTAINER Austin Michne "austinmichne@gmail.com" 
<<<<<<< HEAD
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY . /
WORKDIR /
RUN pip3 install -r requirements.txt
EXPOSE 5000

CMD ["./run_server.sh", "./root_db_password.txt"]
=======
EXPOSE 80

COPY . .
# WORKDIR .

RUN apk add gcc libc-dev linux-headers mariadb-dev

RUN pip install -r requirements.txt

CMD python ./server.py --user "" --password "" --host "" --db "derived"
>>>>>>> Functional API distrobution and dockerization
