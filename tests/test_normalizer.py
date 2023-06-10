from pathlib import Path
import yaml

import pandas as pd

from pl_itn import Normalizer


def load_data(input_fpath: Path):
    assert input_fpath.suffix == ".csv", "Incorrect input file extension!"

    df = pd.read_csv(str(input_fpath), sep=";")
    src = df["src"].tolist()
    ref = df["ref"].tolist()
    return src, ref


def normalize_corpus(test_set_path: str, normalizer: object) -> bool:

    test_set_path = Path(test_set_path)
    not_normalized, reference = load_data(test_set_path)

    correct, incorrect = [], []

    for not_normalized_phrase, reference_phrase in zip(not_normalized, reference):
        pred = normalizer.normalize(not_normalized_phrase)
        message = f"{not_normalized_phrase};{reference_phrase};{pred}"
        if pred == reference_phrase:
            correct.append(message)
        else:
            incorrect.append(message)

    return correct, incorrect


def test_normalizer(config_path: Path):

    normalizer = Normalizer()

    with config_path.open() as f:
        config = yaml.safe_load(f)

    for corpus in config.get("test_sets"):
        # Dataset is defined as List[set_name, set_path, accepted_errors_limit]
        test_set_name, test_set_path, accepted_errors_threshold = corpus
        correct_norm, incorrect_norm = normalize_corpus(test_set_path, normalizer)

        for case in incorrect_norm:
            print(case)

        assert (
            len(incorrect_norm) <= accepted_errors_threshold
        ), f'Number of wrong normalizations for "{test_set_name}" ({len(incorrect_norm)}) is higher than its threshold ({accepted_errors_threshold}).'