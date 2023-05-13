#!/usr/bin/env python

import argparse
from pathlib import Path
import yaml

from tagger.tag import TagFst
from verbalizer.verbalize import VerbalizeFst


def main(config_path: Path, grammars_dir: Path):
    with config_path.open() as f:
        config = yaml.safe_load(f)

    grammars_dir.mkdir(parents=True, exist_ok=True)
    tagger_path = grammars_dir / 'tagger.fst'
    verbalizer_path = grammars_dir / 'verbalizer.fst'

    graph = TagFst(config)
    graph.save_fst(str(tagger_path))

    graph = VerbalizeFst(config)
    graph.save_fst(str(verbalizer_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Build and save to file finite state transducer grammars.'
    )
    parser.add_argument('-c', '--config-path', type=Path, default=f'build_grammar/grammar_config.yaml',
                        help='Grammar configuration file')
    parser.add_argument('-g', '--grammars-dir', type=Path, help="Directory where grammars will be saved.", default=Path("pl_itn/grammars"))
    args = parser.parse_args()

    main(args.config_path, args.grammars_dir)