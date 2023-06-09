# pl_itn
Inverse Text Normalization is an NLP task of changing the spoken form of a phrase to written form, for example:
```
one two three -> 1 2 3
```

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

`pl_itn` is an opensource Polish ITN Python library and REST API for practical applications.

This project is an implementation of [NeMo Inverse Text Normalization](https://arxiv.org/abs/2104.05055) for Polish.

## Table of contents
[Prerequisites](#prerequisites)\
[Setup](#setup)\
[Docker](#docker)\
[Usage](#usage)\
[gRPC service](#grpc-service)\
[restful fastAPI service](#restful-fastapi-service)\
[Building custom grammars](#building-custom-grammars)\
[Documentation](#documentation)\
[Contributing](#contributing)\
[License](#License)\
[References](#References)

## Prerequisites
For [pynini](https://pypi.org/project/pynini/)
- A standards-compliant C++17 compiler (GCC >= 7 or Clang >= 700)
- The compatible recent version of OpenFst built with the grm extensions (see `deps/install_openfst.md`)

## Setup
Make sure to first install prerequisites, especially OpenFST.

### Install from PyPI
```bash
pip install pl_itn
```

### Build from source
```bash
pip install .
```

### Editable install for development
```bash
pip install -e .[dev]
```

### Docker

To build docker image containing pl_itn library use `pl_itn_lib.dockerfile` file.

```bash
docker build -t <IMAGE:TAG> -f <DOCKERFILE> .
```

To build a gRPC service or a restful service for this project, you will need to use the Dockerfiles located in their respective directories. 

 - `grpc_service/`: Contains the Dockerfile and any additional files required to build and run the gRPC service.
 - `restful_service/`: Contains the Dockerfile and any additional files required to build and run the REST service.

To build the gRPC service, navigate to the `grpc_service/` directory and use the provided Dockerfile:

```bash
cd grpc_service/
docker build -t pl-itn-grpc-service .
```

Similarly, to build the REST service, navigate to the `restful_service/` directory and use the corresponding Dockerfile:

```bash
cd grpc_service/
docker build -t pl-itn-rest-service .
```

Official pl-itn images are available in [dockerhub](https://hub.docker.com/repository/docker/cansubmarinesswim/).


## Usage
### Console app
```bash
usage: pl_itn [-h] (-t TEXT | -i) [--tagger TAGGER] [--verbalizer VERBALIZER] [--config CONFIG]
              [--log-level {debug,info}]

Inverse Text Normalization based on Finite State Transducers

options:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Input text
  -i, --interactive     If used, demo will process phrases from stdin interactively.
  --tagger TAGGER
  --verbalizer VERBALIZER
  --config CONFIG       Optionally provide yaml config with tagger and verbalizer paths.
  --log-level {debug,info}
                        return a step back value.
```

```bash
pl_itn -t "jest za pięć druga"
jest 01:55

pl_itn -t "drugi listopada dwa tysiące osiemnastego roku"
2 listopada 2018 roku
```

### Python
```python
>>> from pl_itn import Normalizer
>>> normalizer = Normalizer()
>>> normalizer.normalize("za pięć dwunasta")
'11:55'
```

### Docker

Existing docker image containing pl_itn library is required. For build command refer to [Docker](#docker) section.
```bash
docker run --rm -it <IMAGE:TAG> --help
```

## gRPC Service

gRPC service methods are described in `grpc_service/pl_itn_api/api.proto` file. Docker container is suggested approach for running the service. For build command refer to [Docker](#docker) section.
Service within container serves on port 10010.

Example of building the image and starting the service.
```bash
docker build -t pl_itn_service:test -f grpc_service.dockerfile .
docker run -p 10010:10010 pl_itn_service:test
```

## restful fastAPI Service

Docker container is suggested approach for running the service. For build command refer to [Docker](#docker) section.
To access detailed information about the REST API endpoints, you can refer to the `/openapi.json` endpoint when running the service. 

## Building custom grammars
Custom grammars can be built using `build_grammar/build_grammar.py` script.

There are three demo grammars available:
- not declined cardinal numbers (e.g. "jeden", "dwa", "trzy")
- declined cardinal numbers (e.g. "jednego", "dwóch", "trzech")
- ordinal numbers (e.g. "pierwszy", "druga", "trzecie")

Normalization types can be included and excluded from the grammar through the config file, which is set by default to `build_grammar/grammar_config.yaml`.

```bash
# cardinals_basic_forms: True
# cardinals_declined: True
# ordinals: True

$ python3 build_grammar/build_grammar.py --grammars-dir all

$ pl_itn \
  --tagger all/tagger.fst \
  --verbalizer all/verbalizer.fst \
  -t "Jeden trzech piąta"

1 3 5
```

```bash
# cardinals_basic_forms: True
# cardinals_declined: False
# ordinals: True

$ python3 build_grammar/build_grammar.py --grammars-dir cardinals_basic_ordinals

$ pl_itn \
  --tagger cardinals_basic_ordinals/tagger.fst \
  --verbalizer cardinals_basic_ordinals/verbalizer.fst \
  -t "Jeden trzech piąta"

1 trzech 5
```

```bash
# cardinals_basic_forms: True
# cardinals_declined: False
# ordinals: False

$ python3 build_grammar/build_grammar.py --grammars-dir only_basic_cardinals

$ pl_itn \
  --tagger only_basic_cardinals/tagger.fst \
  --verbalizer only_basic_cardinals/verbalizer.fst \
  -t "Jeden trzech piąta"

1 trzech piąta
```

See [Documentation](#documentation) for more details.

## Documentation

## Contributing

## License

## Rerences
- K. Gorman. 2016. Pynini: A Python library for weighted finite-state grammar compilation. In Proc. ACL Workshop on Statistical NLP and Weighted Automata, 75-80.
- Y. Zhang, E. Bakhturina, K. Gorman, and B. Ginsburg. 2021. NeMo Inverse Text Normalization: From Development To Production.