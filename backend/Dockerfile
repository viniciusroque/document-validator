FROM python:3.10-slim

RUN useradd -ms /bin/bash backend --home /backend

USER backend

ENV HISTFILE=/backend/history/.bash_history

WORKDIR /backend

ENV PYTHONPATH=${PYTHONPATH}/backend/app

CMD [ "tail", "-f", "/dev/null" ]