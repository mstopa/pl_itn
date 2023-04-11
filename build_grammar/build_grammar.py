#!/usr/bin/env python

import argparse
from pathlib import Path
import yaml

# from tagger.tag import TagFst
from verbalizer.verbalize import VerbalizeFst


def main(config_path: Path, tagger_path: Path, verbalizer_path: Path):
    with config_path.open() as f:
        config = yaml.safe_load(f)

    tagger_path.parent.mkdir(parents=True, exist_ok=True)
    verbalizer_path.parent.mkdir(parents=True, exist_ok=True)

    # graph = TagFst(config)
    # graph.write_to_fst(str(tagger_path))

    graph = VerbalizeFst(config)
    graph.write_to_fst(str(verbalizer_path))
 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Build and save to file finite state transducer grammars.'
    )
    parser.add_argument('--tagger', type=Path, help="Tagger graph will be saved to provided path.", default=Path("pl_itn/grammars/tagger.fst"))
    parser.add_argument('--verbalizer', type=Path, help="Verbalizer graph will be saved to provided path.", default=Path("pl_itn/grammars/verbalizer.fst"))    
    parser.add_argument('-c', '--config_path', type=Path, default=f'build_grammar/grammar_config.yaml',
                        help='Grammar configuration file')
    args = parser.parse_args()

    main(args.config_path, args.tagger, args.verbalizer)