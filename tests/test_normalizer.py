import argparse
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from typing import List
import yaml

from pl_itn import Normalizer


def run_tests(config_path: Path):
    with config_path.open() as f:
        config = yaml.safe_load(f)

    normalizer = Normalizer(
        tagger_fst_path="/home/tkurkowski/Tasks/studia/inzynierka/fst_resources/tagger_full.fst",
        verbalizer_fst_path="/home/tkurkowski/Tasks/studia/inzynierka/fst_resources/verbalizer_full.fst",
    )

    results_dir = Path(config.get("test").get("results_dir"))
    results_dir.mkdir(parents=True, exist_ok=True)

    exit_code = 0
    for corpus in config.get("test").get("test_sets"):
        test_passed = run_test(results_dir, corpus, normalizer)
        if not test_passed:
            exit_code = 1

    exit(exit_code)


def run_test(results_dir: Path, corpus: List, normalizer: object) -> bool:
    # Dataset is defined as List[set_name, set_path, accepted_errors_limit]
    corpus_name, input_fpath, accepted_errors_num = corpus
    input_fpath = Path(input_fpath)

    src, ref = load_data(input_fpath)

    correct = []
    incorrect = []

    for index, phrase in enumerate(tqdm(src)):
        pred = normalizer.normalize(phrase)
        message = f"{phrase};{ref[index]};{pred}"
        if pred == ref[index]:
            correct.append(message)
        else:
            incorrect.append(message)

    newline = "\n"  # to avoid syntax error in summary_message: f-string expression part cannot include a backslash
    summary_message = f"""
CORRECT:
{newline.join(correct)}

INCORRECT:
{newline.join(incorrect)}

Correct predictions: {len(correct)} ({round(len(correct) / len(src), 2)})
Incorrect predictions: {len(incorrect)} ({round(len(incorrect) / len(src), 2)})
    """

    print(summary_message)

    results_fpath = results_dir / f"{corpus_name}.txt"
    with results_fpath.open(mode="w", encoding="utf-8") as fwrite:
        fwrite.write(summary_message)

    # for exit code
    return len(incorrect) <= accepted_errors_num


def load_data(input_fpath: Path):
    assert input_fpath.suffix == ".csv", "Incorrect input file extension!"

    df = pd.read_csv(str(input_fpath), sep=";")
    src = df["src"].tolist()
    ref = df["ref"].tolist()
    return src, ref


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test single ITN setup based on its config.")
    parser.add_argument("config_path", type=Path, help="For example configs/default_conf.yaml")

    args = parser.parse_args()
    
    run_tests(args.config_path)
