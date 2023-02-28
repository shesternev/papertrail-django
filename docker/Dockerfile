FROM python:3.10.9-alpine3.17
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /backend
COPY /requirements/requirements.txt .
RUN apk add postgresql-client build-base postgresql-dev
RUN pip install --no-cache-dir -r requirements.txt