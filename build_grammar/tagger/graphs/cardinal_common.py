import pynini
from pynini.lib import pynutil

from common.graph import GraphFst, maybe_delete_space_fst, digit_fst


class UpToThousandFst(GraphFst):
    def __init__(self, unit_fst, teen_fst, ties_fst, hundred_fst) -> None:
        """
        Possible options:
        001 <- [hundred: 0][ties: 0 teens: 0][units: True]
        011 <- [hundred: 0][ties: 0 teens: True][units: 0]
        021 <- [hundred: 0][ties: True teens: 0][units: 1]
        101 <- [hundred: True][ties: 0 teens: 0][units: True]
        111 <- [hundred: True][ties: 0 teens: True][units: 0]
        121 <- [hundred: True][ties: True teens: 0][units: True]
        """
        accept_hundreds_or_insert_zero_fst = pynini.union(hundred_fst, pynutil.insert("0"))
        accept_ties_or_insert_zero_fst = pynini.union(ties_fst, pynutil.insert("0"))
        accept_teens_or_insert_zero_fst = pynini.union(teen_fst, pynutil.insert("00"))
        accept_units_or_insert_zero_fst = pynini.union(unit_fst, pynutil.insert("0"))

        accept_ties_and_units_fst = accept_ties_or_insert_zero_fst + maybe_delete_space_fst + accept_units_or_insert_zero_fst
        accept_either_teens_or_ties_and_units_fst = pynini.union(accept_teens_or_insert_zero_fst, accept_ties_and_units_fst)

        graph = accept_hundreds_or_insert_zero_fst + maybe_delete_space_fst + accept_either_teens_or_ties_and_units_fst

        self._fst = graph.optimize()


remove_leading_zeros_fst = (
    pynutil.delete(pynini.closure("0"))
    + pynini.closure(pynini.difference(digit_fst, "0"), 1)
    + pynini.closure(digit_fst)
)