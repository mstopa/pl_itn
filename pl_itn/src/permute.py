from collections import OrderedDict
import itertools
import logging
from typing import List

logger = logging.getLogger(__name__)


class Permuter:
    def __init__(self, tokens: List[dict]):
        self.tokens = tokens
        self.length = len(tokens)

    def generate_permutations(self):
        """
        Initiate generate_permutations_recursive() on tokens
        with no processed_left_string.
        """
        return self.generate_permutations_recursive(processed_left_string = "", index = 0)

    def generate_permutations_recursive(self, processed_left_string, index):
            """
            One by one sequentially, each input substructure generates permutations.
            Each permutation starts a new output instance.
            """
            if index >= self.length:    # no more input to process, exit recurency
                yield processed_left_string
            
            else:
                cursor_permutations = self._permute(self.tokens[index])

                for permutation in cursor_permutations:
                    yield from self.generate_permutations_recursive(
                            processed_left_string + permutation, index + 1
                        )

    def _permute(self, token):
        results = []

        permutations = itertools.permutations(token.items())
        for permutation in permutations:

            # serialize nested list-dict structure to a flat list of strings
            converted_permutation = [""] # output structure: list of strings

            for key, value in permutation:
                if isinstance(value, str):
                    pattern = [f"{key}: \"{value}\" "]
                    converted_permutation = ["".join(x) for x in itertools.product(converted_permutation, pattern)]
                elif isinstance(value, bool):
                    pattern = [f"{key}: {value} "]
                    converted_permutation = ["".join(x) for x in itertools.product(converted_permutation, pattern)]
                elif isinstance(value, OrderedDict):
                    recursive_permutation = self._permute(value)
                    prefix = [f" {key} {{ "]
                    suffix = [" } "]
                    converted_permutation = ["".join(x) for x in itertools.product(converted_permutation, prefix, recursive_permutation, suffix)]
                else:
                    logger.error("Permuter error! Substructure type is incorrect, something went really wrong.")
                    raise ValueError()

            logger.debug(converted_permutation)
            results.extend(converted_permutation)

        return results