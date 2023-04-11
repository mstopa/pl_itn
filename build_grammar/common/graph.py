import pynini

class GraphFst:
    def __init__(self) -> None:
        pass
    
    @property
    def fst(self) -> pynini.Fst:
        return self._fst
    
    def write_to_fst(self, path: str) -> None:
        self._fst.write(path)