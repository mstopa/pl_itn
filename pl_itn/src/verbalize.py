import logging
import pynini

logger = logging.getLogger(__name__)


class Verbalizer:
    def __init__(self, fst_path):
        self.verbalizer = pynini.Fst.read(str(fst_path))

    def verbalize(self, tags_permutations):
        for tagged_text_permutation in tags_permutations:
            tagged_text_permutation = pynini.escape(tagged_text_permutation)
            logger.debug(tagged_text_permutation)
            lattice = tagged_text_permutation @ self.verbalizer

            if lattice.num_states() == 0:
                # this permutation is not syntactically correct (not foreseen by verbalizer)
                continue
            else:
                text = pynini.shortestpath(
                    lattice, nshortest=1, unique=True).string()
                logger.debug(text)
                return text
        # no syntactically correct permutation found
        logger.error("Verbalizer returned no output")
        raise ValueError()