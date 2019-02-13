FROM ubuntu:18.04
MAINTAINER Austin Michne "austinmichne@gmail.com" 
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY . /
WORKDIR /
RUN pip3 install -r requirements.txt
EXPOSE 5000

CMD ["./run_server.sh", "./root_db_password.txt"]
