import pynini
from pynini.lib import utf8 as pynini_utf8
from pynini.lib import pynutil

class GraphFst:
    def __init__(self) -> None:
        pass
    
    @property
    def fst(self) -> pynini.Fst:
        return self._fst
    
    def write_to_fst(self, path: str) -> None:
        self._fst.write(path)


char_fst = pynini_utf8.VALID_UTF8_CHAR
not_quote_fst = pynini.difference(char_fst, r'"')

whitespace_fst = pynini.union(" ", "\t", "\n", "\r", u"\u00A0")
not_whitespace_fst = pynini.difference(char_fst, whitespace_fst)
surely_delete_space_fst = pynutil.delete(pynini.closure(whitespace_fst, 1))