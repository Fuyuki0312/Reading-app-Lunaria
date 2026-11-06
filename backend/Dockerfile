FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN python -m pip install --no-cache-dir torch==2.5.1
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY chroma_db ./chroma_db
