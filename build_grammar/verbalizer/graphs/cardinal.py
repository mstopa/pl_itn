from pynini.lib import utf8
import pynini

from common.graph import GraphFst
from common.rule_labels import lstrip_rule_label, rstrip_rule_label

class CardinalFst(GraphFst):
    """
    Finite state transducer for verbalizing cardinal
    e.g. cardinal { integer: "23" negative: "-" } -> -23
    """
    def __init__(self) -> None:
        graph = pynini.closure(utf8.VALID_UTF8_CHAR)
        
        transformation = (
            lstrip_rule_label("name")
            + graph
            + rstrip_rule_label()
        )

        self._fst = transformation.optimize()