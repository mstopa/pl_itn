FROM continuumio/miniconda3:22.11.1

RUN conda install -c conda-forge pynini

WORKDIR pl_itn
COPY . . 

RUN pip install . ; \
    cd restful_service ; \
    pip install .

ENV FST_DIR=/fst_models
ENV CONSOLE_LOG_LEVEL=INFO
ENV FILE_LOG_LEVEL=INFO
ENV FILE_LOG_DIR=/logs

EXPOSE 8000
ENTRYPOINT ["uvicorn", "pl_itn_service.service:app", "--host", "0.0.0.0", "--port", "8000" ]

