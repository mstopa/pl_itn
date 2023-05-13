import pynini

from common.graph import GraphFst, not_quote_fst, surely_delete_space_fst
from common.rule_labels import lstrip_rule_label, rstrip_rule_label
from common.class_labels import lstrip_class_label, rstrip_class_label


class CardinalFst(GraphFst):
    """
    Finite state transducer for verbalizing cardinal
    e.g. cardinal { integer: "23" negative: "-" } -> -23
    """
    def __init__(self) -> None:
        maybe_remove_sign_fst = pynini.closure(
            (
                lstrip_rule_label("negative")
                + not_quote_fst
                + rstrip_rule_label()
                + surely_delete_space_fst
            ),
            0, 1
        )

        integer_fst = (
            lstrip_rule_label("integer")
            + pynini.closure(not_quote_fst)
            + rstrip_rule_label()
        )

        graph = maybe_remove_sign_fst + integer_fst

        transformation = (
            lstrip_class_label("cardinal")
            + graph
            + rstrip_class_label()
        )

        self.fst = transformation.optimize()