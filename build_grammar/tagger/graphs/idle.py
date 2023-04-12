import pynini

from common.graph import GraphFst, not_whitespace_fst
from common.rule_labels import add_left_rule_label, add_right_rule_label


class IdleFst(GraphFst):
    def __init__(self):
        graph = pynini.closure(not_whitespace_fst, 1)

        transformation = (
            add_left_rule_label("name")
            + graph
            + add_right_rule_label()
        )

        self._fst = transformation.optimize()