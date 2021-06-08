FROM python:3.9-slim-buster

RUN pip install bitrise-reports --upgrade

WORKDIR /reports/

ENTRYPOINT ["bitrise-reports"]
