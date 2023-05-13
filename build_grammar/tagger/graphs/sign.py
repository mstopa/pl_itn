import pynini
from common.graph import GraphFst
from common.rule_labels import add_left_rule_label, add_right_rule_label


class SignFst(GraphFst):
    def __init__(self):

        graph = pynini.cross("minus", "-")

        transformation = (
            add_left_rule_label("negative")
            + graph
            + add_right_rule_label()
        )

        self.fst = transformation.optimize()