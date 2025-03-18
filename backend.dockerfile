
FROM python:3.9-slim


ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


WORKDIR /app


RUN pip install poetry


COPY pyproject.toml poetry.lock /app/


RUN poetry install --no-dev

RUN pip install uvicorn gunicorn


COPY . /app


EXPOSE 8000


CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]

