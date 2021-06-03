FROM python:3.8
LABEL maintainer="svengerlach@me.com"

RUN pip install pipenv

ENV WORKDIR="/usr/local/src/app"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR ${WORKDIR}
COPY Pipfile Pipfile.lock ${WORKDIR}
RUN pipenv install --system --ignore-pipfile
COPY . .

CMD ["python", "alien_invasion.py"]