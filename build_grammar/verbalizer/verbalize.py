import pynini

from common.graph import GraphFst
from common.class_labels import lstrip_class_label, rstrip_class_label

from verbalizer.graphs.cardinal import CardinalFst
from verbalizer.graphs.idle import IdleFst
from verbalizer.graphs.whitelist import WhitelistFst


class VerbalizeFst(GraphFst):
    """
    Finite state transducer that verbalizes an entire sentence, e.g.
    tokens { name: "its" } tokens { time { hours: "12" minutes: "30" } } tokens { name: "now" } -> its 12:30 now
    """
    def __init__(self, config: dict) -> None:
        self.config = config
        
        cardinal = CardinalFst()
        # ordinal = OrdinalFst()
        whitelist = WhitelistFst()
        idle = IdleFst()

        graph = (
            cardinal.fst
            # | ordinal.fst
            | whitelist.fst
            | idle.fst
        )

        transformation = (
            lstrip_class_label("tokens")
            + graph
            + rstrip_class_label()
        )

        transformations = (
            pynini.closure(transformation, 1)
        )

        self._fst = transformations.optimize()