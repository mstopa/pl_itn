import pynini

from common.graph import GraphFst
from common.class_labels import add_left_class_label, add_right_class_label

from tagger.graphs.idle import IdleFst
# from tagger.graphs.cardinal import CardinalFst
# from tagger.graphs.ordinal import OrdinalFst
# from tagger.graphs.whitelist import WhitelistFst


class TagFst(GraphFst):
    """
    Finite state transducer that verbalizes an entire sentence, e.g.
    tokens { name: "its" } tokens { time { hours: "12" minutes: "30" } } tokens { name: "now" } -> its 12:30 now
    """
    def __init__(self, config: dict) -> None:
        self.config = config

        # idle path - this graph accepts any sequence with no normalization
        idle = IdleFst()
        
        # # user defined tokens that will never be normalized
        # whitelist = WhitelistFst()
        
        # # ["jeden", "dwa", "trzy", "sto piętnaście", ...]
        # cardinal_basic_forms = CardinalBasicFst()
        
        # # ["jedno", "jednych", "dwiema", "trzech", "stoma", ...]
        # cardinal_declined = CardinalDeclinedFst(cardinal_basic_forms)
        
        # # ["pierwszy", "drugi", "trzecia", "sto piąte"]
        # ordinal = OrdinalFst(cardinal_basic_forms)

        graph = idle.fst        
        # graph = (
        #     pynutil.add_weight(idle.fst, 100)
        #     | pynutil.add_weight(whitelist.fst, 1.01)
        # )
        
        # if maybe_fetch(config, "cardinals_basic_forms"):
        #     graph |= pynutil.add_weight(cardinal_basic_forms.fst, 1.1)
        # if maybe_fetch(config, "cardinals_declined"):
        #     graph |= pynutil.add_weight(cardinal_declined_graph.fst, 1.1)
        # if maybe_fetch(config, "ordinals"):
        #     graph |= pynutil.add_weight(ordinal_graph.fst, 1.1)

        transformation = (
            add_left_class_label("tokens")
            + graph
            + add_right_class_label()
        )

        # # special, universal graph for punctuation marks
        # punctuation = PunctuationFst()

        transformations = (
            pynini.closure(transformation, 1)
        )

        self._fst = transformations.optimize()