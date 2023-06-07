import pandas as pd
from pathlib import Path
from tqdm import tqdm
import yaml
import pytest

from pl_itn import Normalizer

def _get_test_config_files(config_dir: Path = Path(__file__).resolve().parent / "configs"):
    return [config for config in config_dir.glob("*") if config.is_file()]

@pytest.mark.parametrize("config_path", _get_test_config_files())
def test_normalizer(config_path: Path, save_results):

    normalizer = Normalizer()

    with config_path.open() as f:
        config = yaml.safe_load(f)

    if save_results:
        results_dir = Path(config.get("test").get("results_dir"))
        results_dir.mkdir(parents=True, exist_ok=True)

    for corpus in config.get("test").get("test_sets"):
        # Dataset is defined as List[set_name, set_path, accepted_errors_limit]
        test_set_name, test_set_path, accepted_errors_threshold = corpus
        correct_norm, incorrect_norm = normalize_corpus(test_set_path, normalizer)

        if save_results:
            _save_results_to_file(results_dir, test_set_name, correct_norm, incorrect_norm) 

        assert len(incorrect_norm) <= accepted_errors_threshold, f"Number of wrong normalizations for \"{test_set_name}\" ({len(incorrect_norm)}) is higher than its threshold ({accepted_errors_threshold})."


def _save_results_to_file(results_dir: Path, results_file_name: str, correct_norm: list[str], incorrect_norm: list[str]):
    results_fpath = results_dir / f"{results_file_name}.txt"
    correct_lines = "\n".join(correct_norm)
    incorrect_lines = "\n".join(incorrect_norm)

    with results_fpath.open(mode="w", encoding="utf-8") as f:
        f.write(f"CORRECT:\n")
        f.write(f"{correct_lines}\n\n")
        f.write(f"INCORRECT\n")
        f.write(f"{incorrect_lines}\n\n")
        f.write(f"Correct predictions: {len(correct_lines)}\n")
        f.write(f"Incorrect predictions: {len(incorrect_lines)}")

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

def load_data(input_fpath: Path):
    assert input_fpath.suffix == ".csv", "Incorrect input file extension!"

    df = pd.read_csv(str(input_fpath), sep=";")
    src = df["src"].tolist()
    ref = df["ref"].tolist()
    return src, ref