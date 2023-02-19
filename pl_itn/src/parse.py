from collections import OrderedDict
import logging
import re
from typing import List

logger = logging.getLogger(__name__)


class TokenParser:
    """
    Parses tokenized/classified text, e.g. 
    'tokens { money { integer: "20" currency: "$" } } tokens { name: "left"}'

    Args
        text: tokenized text
    """
    def __init__(self):
        pass

    def parse(self, text) -> List[dict]:
        parsed_tokens = []

        chunks = text.split("tokens")
        chunks_with_length = [c for c in chunks if len(c)]

        for token in chunks_with_length:
            current_level_dict = OrderedDict()
            current_level_dict["tokens"] = self.parse_recursively(token)
            parsed_tokens.append(current_level_dict)

        logger.debug(parsed_tokens)
        return parsed_tokens

    def strip_braces_and_whitespaces(self, text):
        text = text.strip()
        text = text.lstrip("{")
        text = text.rstrip("}")
        text = text.strip()
        return text

    def parse_final_leaf(self, text):
        text = self.strip_braces_and_whitespaces(text)
        keywords = re.findall(r"(\S+): ", text)
        values = re.findall(r"\"([^\"]+)\"", text)

        if len(keywords) != len(values):
            logger.error("Parsing tagged text into tokens failed.")
            raise ValueError()

        for index, keyword in enumerate(keywords):
            yield((keyword, values[index]))

    def parse_recursively(self, text):
        text = self.strip_braces_and_whitespaces(text)
        current_level_dict = OrderedDict()

        if '{' not in text:  # no nested dict
            for keyword, value in self.parse_final_leaf(text):
                current_level_dict[keyword] = value

        else:
            keyword, text = text.split('{', 1)
            keyword = keyword.strip()
            current_level_dict[keyword] = self.parse_recursively(text)

        return current_level_dict
