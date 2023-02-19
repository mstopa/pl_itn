import logging
import pynini

logger = logging.getLogger(__name__)


class Tagger():
    def __init__(self, fst_path):
        self.fst_tagger = pynini.Fst.read(str(fst_path))

    def tag(self, text):
        text = pynini.escape(text)
        text = self.tag_with_fst(text)
        logger.debug(text)

        if text is None:
            logger.error("Tagger returned no output.")
            raise ValueError()
        return text

    def tag_with_fst(self, text):
        lattice = text @ self.fst_tagger
        return pynini.shortestpath(lattice, nshortest=1, unique=True).string()