import pynini

from common.graph import GraphFst, not_quote_fst
from common.rule_labels import lstrip_rule_label, rstrip_rule_label


class IdleFst(GraphFst):
    """
    Path for accepting plain tokens with no transformations.
    """
    def __init__(self) -> None:
        transformation = (
            lstrip_rule_label("name")
            + pynini.closure(not_quote_fst)
            + rstrip_rule_label()
        )
        self.fst = transformation.optimize()