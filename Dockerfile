FROM python:3.9.2
RUN mkdir /todo
WORKDIR /todo
ADD . /todo
RUN pip3 install -r requirements.txt
EXPOSE 8001
