FROM python:3.10-slim

WORKDIR /pl_itn_service
COPY . .

RUN pip install .
EXPOSE 10010
ENTRYPOINT ["pl_itn_service"]
