FROM python:3.10-slim

RUN useradd -ms /bin/bash backend --home /backend

USER backend

ENV HISTFILE=/backend/history/.bash_history

WORKDIR /backend
COPY requirements* /backend/backend/
RUN pip install --upgrade pip && pip install -r backend/requirements-dev.txt

ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH=${PYTHONPATH}/backend/backend

CMD ["python", "-m", "uvicorn", "backend.app.api:app", "--host", "0.0.0.0", "--reload"]