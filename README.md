# pl_itn
Inverse Text Normalization is an NLP task of changing the spoken form of a phrase to written form, for example:
```
one two three -> 1 2 3
```

`pl_itn` is an opensource Polish ITN Python library and REST API for practical applications.

This project is an implementation of [NeMo Inverse Text Normalization](https://arxiv.org/abs/2104.05055) for Polish.

## Table of contents
[Prerequisites](#prerequisites)\
[Setup](#setup)\
[Usage](#usage)\
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

```bash
python3 -m venv .venv
source .venv/bin/activate | source .venv/Scripts/activate
pip install wheel
pip install .
```

## Usage
### Console app
```bash
usage: pl_itn [-h] (-t TEXT | -i) [--tagger TAGGER] [--verbalizer VERBALIZER] [--config CONFIG]
              [--log_level {debug,info}] [-d]

Inverse Text Normalization based on Finite State Transducers

options:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Input text
  -i, --interactive     If used, demo will process phrases from stdin interactively.
  --tagger TAGGER
  --verbalizer VERBALIZER
  --config CONFIG       Optionally provide yaml config with tagger and verbalizer paths.
  --log_level {debug,info}
  -d, --debug_mode      If used, process will be interrupted on runtime errors, else it will
                        return a step back value.
```

```bash

```

### Python
```python
```


## Documentation

## Contributing

## License

## Rerences
- K. Gorman. 2016. Pynini: A Python library for weighted finite-state grammar compilation. In Proc. ACL Workshop on Statistical NLP and Weighted Automata, 75-80.
- Y. Zhang, E. Bakhturina, K. Gorman, and B. Ginsburg. 2021. NeMo Inverse Text Normalization: From Development To Production.