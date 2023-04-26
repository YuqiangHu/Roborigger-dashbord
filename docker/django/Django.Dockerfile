FROM python:3.9.6-slim-buster
ENV POETRY_VERSION=1.1.5
RUN apt-get upgrade -y
RUN apt-get update && apt-get install -y curl  git  graphviz libgraphviz-dev 
WORKDIR /code
COPY ./backend /code/
COPY ./docker/django/django.sh /scripts/django.sh
RUN chmod +x /scripts/django.sh
COPY ./backend/requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 manage.py migrate
# RUN python3 manage.py collectstatic --noinput
# RUN python3 manage.py runserver