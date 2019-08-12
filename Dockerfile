FROM ubuntu:16.04

RUN apt-get update -y --fix-missing

RUN apt-get install -y cmake 
RUN apt-get install -y python3-pip
RUN apt-get install -y python-virtualenv

COPY . /
WORKDIR /

RUN virtualenv -p python3 mario

RUN /bin/bash -c "source mario/bin/activate"


# ADD $PWD/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
EXPOSE 5001
CMD ["python3", "server.py"]