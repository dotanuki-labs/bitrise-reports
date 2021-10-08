# Building

FROM python:3.9-slim-buster as builder

RUN apt-get update && \
	apt-get install -y make && \
	python -m pip install --upgrade --no-cache-dir pip && \
	pip install poetry

WORKDIR /tmp

COPY . .

RUN poetry build && find ./dist -name "*.tar.gz" -exec mv {} /tmp/app.tar.gz  \;


# Packaging

FROM python:3.9-slim-buster

WORKDIR /reports/

COPY --from=builder /tmp/app.tar.gz .

RUN python -m pip install --upgrade --no-cache-dir pip && \
	pip install --no-cache-dir app.tar.gz && \
	rm app.tar.gz

ENTRYPOINT ["bitrise-reports"]
