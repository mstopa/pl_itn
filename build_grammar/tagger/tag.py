import pynini
from pynini.lib import pynutil

from common.graph import GraphFst, accept_space_fst
from common.class_labels import add_left_class_label, add_right_class_label

from tagger.graphs.idle import IdleFst
from tagger.graphs.manual import ManualFst
from tagger.graphs.cardinal_basic import CardinalBasicFst
from tagger.graphs.cardinal_declined import CardinalDeclinedFst
# from tagger.graphs.ordinal import OrdinalFst


class TagFst(GraphFst):
    """
    Finite state transducer that verbalizes an entire sentence, e.g.
    tokens { name: "its" } tokens { time { hours: "12" minutes: "30" } } tokens { name: "now" } -> its 12:30 now
    """
    def __init__(self, config: dict) -> None:
        self.config = config

        # idle path - this graph accepts any sequence with no normalization
        idle = IdleFst()
        
        # transformations defined manually by the user
        # ignored in other transformations
        manual = ManualFst()
        
        # ["jeden", "dwa", "trzy", "sto piętnaście", ...]
        cardinal_basic_forms = CardinalBasicFst()
        
        # ["jedno", "jednych", "dwiema", "trzech", "stoma", ...]
        cardinal_declined = CardinalDeclinedFst(cardinal_basic_forms)
        
        # # ["pierwszy", "drugi", "trzecia", "sto piąte"]
        # ordinal = OrdinalFst(cardinal_basic_forms)
     
        graph = (
            pynutil.add_weight(idle.fst, 100)
            | pynutil.add_weight(manual.fst, 1.01)
        )
        
        if config.get("cardinals_basic_forms"):
            graph |= pynutil.add_weight(cardinal_basic_forms.fst, 1.1)
        if config.get("cardinals_declined"):
            graph |= pynutil.add_weight(cardinal_declined.fst, 1.1)
        # if config.get("ordinals"):
        #     graph |= pynutil.add_weight(ordinal_graph.fst, 1.1)

        transformation = (
            add_left_class_label("tokens")
            + graph
            + add_right_class_label()
        )

        transformations = transformation + pynini.closure(accept_space_fst + transformation)

        self._fst = transformations.optimize()