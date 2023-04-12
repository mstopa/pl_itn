import pynini

from common.graph import GraphFst, not_quote_fst
from common.rule_labels import lstrip_rule_label, rstrip_rule_label
from common.class_labels import lstrip_class_label, rstrip_class_label


class OrdinalFst(GraphFst):
    def __init__(self) -> None:
        integer_fst = (
            lstrip_rule_label("integer")
            + pynini.closure(not_quote_fst)
            + rstrip_rule_label()
        )

        transformation = (
            lstrip_class_label("ordinal")
            + integer_fst
            + rstrip_class_label()
        )

        self._fst = transformation.optimize()