FROM continuumio/miniconda3:22.11.1

RUN conda install -c conda-forge pynini

WORKDIR pl_itn
COPY . . 

RUN pip install .
ENTRYPOINT ["pl_itn"]
