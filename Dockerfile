#ARG PARALLEL_JOBS=8
#ARG OPENFST_VERSION=1.8.2

#FROM gcc:12.2.0 AS build-openfst

#WORKDIR /build
#
#ARG OPENFST_VERSION
#ARG PARALLEL_JOBS

#ENV CXXFLAGS="-fPIC"
#RUN { \
#    # apt update ; \
#    wget https://www.openfst.org/twiki/pub/FST/FstDownload/openfst-${OPENFST_VERSION}.tar.gz || exit 1; \
#    tar -xvzf openfst-${OPENFST_VERSION}.tar.gz && cd openfst-${OPENFST_VERSION} ; \
#    ./configure --enable-far=true -enable-static=yes --enable-shared=no --enable-grm=true --prefix=/release/openfst ; \
#    make -j ${PARALLEL_JOBS} ; \
#    make install ; \
#}

#FROM python:3.10-slim

#COPY --from=build-openfst /release/openfst /opt/openfst

#WORKDIR /pl_itn
#COPY . .

#RUN { \
#    cp -r /opt/openfst/bin/* /usr/local/bin/ ; \
#    cp -r /opt/openfst/lib/* /usr/local/lib/ ; \
#    cp -r /opt/openfst/include/* /usr/local/include ; \
#    rm -rf /opt/openfst ; \
#}
#
#RUN { \
#    apt update ; \
#    apt install -y gcc g++ graphviz ; \
#    pip install --upgrade pip ; \
#    pip install cython ; \
#    # pip install . ; \
#}

FROM continuumio/miniconda3:22.11.1

WORKDIR pl_itn
COPY . . 

#RUN /bin/true\
#    && /usr/bin/poetry config virtualenvs.create false \
#    && poetry install --no-interaction \
#    && rm -rf /root/.cache/pypoetry


RUN conda install -c conda-forge pynini
# RUN pip install .
