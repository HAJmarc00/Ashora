FROM python:3.12
LABEL maintainer="Arshia Nozamani | https://github.com/HAJmarc00"

ENV PYTHONUNBUFFERED=1

RUN mkdir /Ashora
WORKDIR /Ashora

COPY . /Ashora/
ADD requirements/requirements.txt /Ashora/

RUN apt-get update && \
    apt-get install -y --fix-missing build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements/requirements.txt

RUN python manage.py collectstatic --noinput || true
RUN python manage.py migrate || true

CMD ["gunicorn", "--chdir", "/Ashora", "--bind", ":8000", "Ashora.wsgi:application"]