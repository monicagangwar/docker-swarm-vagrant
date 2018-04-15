FROM debian:stable-slim

ENV FLASK_APP app.py

RUN apt-get update && \
    apt-get install -y python python-pip --no-install-recommends python-setuptools && \
    pip install Flask

ADD app /home/app/

WORKDIR /home/app

EXPOSE 8000

CMD python -m flask run --port=8000 --host=0.0.0.0
