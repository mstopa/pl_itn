import pynini

from common.graph import GraphFst, accept_space_fst
from common.class_labels import lstrip_class_label, rstrip_class_label

from verbalizer.graphs.cardinal import CardinalFst
from verbalizer.graphs.ordinal import OrdinalFst
from verbalizer.graphs.idle import IdleFst
from verbalizer.graphs.manual import ManualFst


class VerbalizeFst(GraphFst):
    """
    Finite state transducer that verbalizes an entire sentence, e.g.
    tokens { name: "its" } tokens { time { hours: "12" minutes: "30" } } tokens { name: "now" } -> its 12:30 now
    """
    def __init__(self, config: dict) -> None:
        self.config = config
        
        cardinal = CardinalFst()
        ordinal = OrdinalFst()
        whitelist = ManualFst()
        idle = IdleFst()

        graph = whitelist.fst | idle.fst

        if config.get("cardinals_basic_forms") or config.get("cardinals_declined"):
            graph |= cardinal.fst
        if config.get("ordinals"):
            graph |= ordinal.fst

        transformation = (
            lstrip_class_label("tokens")
            + graph
            + rstrip_class_label()
        )

        transformations = transformation + pynini.closure(accept_space_fst + transformation)

        self.fst = transformations.optimize()