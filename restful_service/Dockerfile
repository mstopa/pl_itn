FROM python:3.10-slim

WORKDIR /restful_service
COPY . . 

RUN pip install .

ENV FST_DIR=/fst_models
ENV CONSOLE_LOG_LEVEL=INFO
ENV FILE_LOG_LEVEL=INFO
ENV FILE_LOG_DIR=/logs

EXPOSE 8000
ENTRYPOINT ["uvicorn", "pl_itn_service.service:app", "--host", "0.0.0.0", "--port", "8000" ]