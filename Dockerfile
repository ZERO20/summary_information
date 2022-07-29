FROM python:3.9.13-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev python-dev gcc

COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code

CMD ["sleep", "infinity"]
