FROM python:3.12

WORKDIR /app

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY /hw3/requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY ../lecture_2 /app/

COPY ../pyproject.toml /app/
COPY ../poetry.lock /app/
RUN poetry install
COPY ../. .
ENV PORT=5050

EXPOSE $PORT

CMD ["poetry", "run", "uvicorn", "lecture_2.hw.shop_api.main:app", "--port", "5050", "--host", "0.0.0.0"]