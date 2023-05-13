import pynini
from pynini.lib import utf8 as pynini_utf8
from pynini.lib import pynutil

class GraphFst:
    def __init__(self) -> None:
        self._fst = None
    
    @property
    def fst(self) -> pynini.Fst:
        return self._fst
    
    @fst.setter
    def fst(self, fst: pynini.Fst) -> None:
        self._fst = fst
    
    def save_fst(self, path: str) -> None:
        self._fst.write(path)


char_fst = pynini_utf8.VALID_UTF8_CHAR
not_quote_fst = pynini.difference(char_fst, r'"')

whitespace_fst = pynini.union(" ", "\t", "\n", "\r", u"\u00A0")
not_whitespace_fst = pynini.difference(char_fst, whitespace_fst)
surely_delete_space_fst = pynutil.delete(pynini.closure(whitespace_fst, 1))
maybe_delete_space_fst = pynutil.delete(pynini.closure(whitespace_fst, 0, 1))
insert_space_fst = pynutil.insert(" ")

lstrip_whitespace_fst = pynini.cdrewrite("", "", whitespace_fst, "")
accept_space_fst = pynini.cross(whitespace_fst, " ")

digit_fst = pynini.union("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
non_zero_number = pynini.closure(digit_fst) + pynini.closure(pynini.difference(digit_fst, "0"), 1) + pynini.closure(digit_fst)