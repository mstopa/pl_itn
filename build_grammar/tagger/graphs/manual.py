import pynini
from common.graph import GraphFst
from common.rule_labels import add_left_rule_label, add_right_rule_label


class ManualFst(GraphFst):
    def __init__(self):

        graph = pynini.string_file("build_grammar/tagger/data/manual.tsv")

        transformation = (
            add_left_rule_label("manual")
            + graph
            + add_right_rule_label()
        )

        self.fst = transformation.optimize()