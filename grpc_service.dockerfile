FROM continuumio/miniconda3:22.11.1

RUN conda install -c conda-forge pynini

WORKDIR pl_itn
COPY . . 

RUN pip install . ; \
    cd grpc_service ; \
    pip install .

EXPOSE 10010
ENTRYPOINT ["pl_itn_service"]

