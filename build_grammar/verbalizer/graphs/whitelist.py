from common.graph import GraphFst
from verbalizer.graphs.idle import IdleFst


class WhitelistFst(GraphFst):
    """
    Path for excluding whitelisted tokens from transformation.
    """
    def __init__(self) -> None:
        alias = IdleFst()
        self._fst = alias.fst