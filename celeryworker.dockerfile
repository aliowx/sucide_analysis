FROM dr2.parswitch.com/devops/python:3-10
WORKDIR /app/
ENV PYTHONPATH=/app

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./app/pyproject.toml ./app/poetry.lock* /app/

RUN pip install poetry fastapi uvicorn gunicorn
RUN poetry config virtualenvs.create false
RUN poetry export -f requirements.txt --without-hashes --output /app/requirements.txt
RUN pip install -r requirements.txt

ENV C_FORCE_ROOT=1
COPY ./app/worker-start.sh /worker-start.sh

COPY ./app /app

CMD ["/bin/bash", "/worker-start.sh"]

