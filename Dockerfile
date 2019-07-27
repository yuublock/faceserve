FROM python:alpine3.7
# ENTRYPOINT [ “/bin/bash”, “-c” ]

COPY . /app
WORKDIR /app

RUN python3 -m venv env

RUN echo 'source env/bin/activate'
RUN echo 'pip install -r /app/requirements.txt'
EXPOSE 5001
CMD "python ./server.py"
