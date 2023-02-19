import logging
from pathlib import Path
import re

from pl_itn.src.tag import Tagger
from pl_itn.src.parse import TokenParser
from pl_itn.src.permute import Permuter
from pl_itn.src.verbalize import Verbalizer
from pl_itn.src.restore_whitespace import WhitespaceRestorer, punctuation
from pl_itn.src.restore_uppercase import UppercaseRestorer

logger = logging.getLogger(__name__)

package_root = Path(__file__).parents[1]

class Normalizer:
    def __init__(self,
                 tagger_fst_path: Path = package_root / "grammars/tagger.fst",
                 verbalizer_fst_path: Path = package_root / "grammars/verbalizer.fst",
                 debug_mode: bool = False
                 ):
        # Thread safe objects
        self.tagger = Tagger(tagger_fst_path)
        self.parser = TokenParser()
        self.verbalizer = Verbalizer(verbalizer_fst_path)
        self.debug_mode = debug_mode

        # Objects to initialize in self.normalize() per session due to race conditions:
        # Permuter, UppercaseRestorer

    def normalize(self, text: str) -> str:
        logger.debug(f"input: {text}")

        preprocessed_text = self.pre_process(text)

        if len(preprocessed_text) == 0:
            logger.info("Empty input string")
            return text
        else:
            logger.debug(f"pre_process(): {preprocessed_text}")

        try:
            tagged_text = self.tagger.tag(preprocessed_text)
            tokens = self.parser.parse(tagged_text)
            tags_reordered = Permuter(tokens).generate_permutations()
            verbalized_text = self.verbalizer.verbalize(tags_reordered)
            postprocessed_text = self.post_process(verbalized_text)
            uppercase_restored = UppercaseRestorer(text, postprocessed_text).run()
            whitespaces_restored = WhitespaceRestorer(text, uppercase_restored, tokens).run()
            return whitespaces_restored 
        
        except ValueError:
            if self.debug_mode:
                raise
            else:
                return text
       
    def pre_process(self, text: str):
        text = text.lower()
        
        # Add spaces around punctuation
        for punct in punctuation:
            text = text.replace(punct, f" {punct} ")
        
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        text = text.strip()
        return text

    def post_process(self, text):
        text = re.sub(r' +', ' ', text)
        text = text.strip()
        return text