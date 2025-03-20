FROM python:3.12-slim

ARG VERSION
ENV PYTHONPATH=$PYTHONPATH:/app/
ENV SYSTEM_VERSION=$VERSION

COPY . ./app

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    nano \
    curl \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["make", "run_app"]
