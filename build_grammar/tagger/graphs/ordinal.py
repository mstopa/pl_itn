import pynini
from pynini.lib import pynutil

from common.graph import GraphFst, accept_space_fst, maybe_delete_space_fst
from common.rule_labels import add_left_rule_label, add_right_rule_label
from common.class_labels import add_left_class_label, add_right_class_label

from tagger.graphs.sign import SignFst
from tagger.graphs.cardinal_common import UpToHundredFst, UpToThousandFst, remove_leading_zeros_fst


class OrdinalFst(GraphFst):
    def __init__(self, cardinal_basic_fst: pynini.Fst):
        graph = pynini.Fst()

        for gender in ("fem",  "masc",  "neut"):
            for case in ("nom", "gen", "dat", "acc", "inst", "loc"):
                graph |= GenderCaseOrdinalFst(gender, case, cardinal_basic_fst).fst

        transformation = (
            add_left_rule_label("integer")
            + graph
            + add_right_rule_label()
        )

        sign_fst = SignFst().fst
        transformation = pynini.closure(sign_fst + accept_space_fst, 0, 1) + transformation

        transformation = (
            add_left_class_label("cardinal")
            + transformation
            + add_right_class_label()
        )  

        self._fst = transformation.optimize()


class GenderCaseOrdinalFst(GraphFst):
    def __init__(self, gender: str, case: str, basic_cardinal_fst: GraphFst) -> None:
        data_root = f"build_grammar/tagger/data/ordinal/{gender}/{case}/"

        unit_fst = pynini.string_file(data_root + "digit.tsv")
        teen_fst = pynini.string_file(data_root + "teen.tsv")
        ties_fst = pynini.string_file(data_root + "ties.tsv")

        up_to_hundred_fst = UpToHundredFst(unit_fst, teen_fst, ties_fst).fst

        above_hundred_fst = AboveHundredFst(case, gender, "hundred", basic_cardinal_fst.hundred_fst)
        above_thousand_fst = AboveHundredFst(case, gender, "thousand", basic_cardinal_fst.above_thousand_fst)
        above_million_fst = AboveHundredFst(case, gender, "million", basic_cardinal_fst.above_million_fst)
        above_billion_fst = AboveHundredFst(case, gender, "billion", basic_cardinal_fst.hundred_fst)

        graph = (
            above_billion_fst.fst
            + maybe_delete_space_fst
            + above_million_fst.fst
            + maybe_delete_space_fst
            + above_thousand_fst.fst
            + maybe_delete_space_fst
            + above_hundred_fst.fst
            + maybe_delete_space_fst
            + up_to_hundred_fst 
        )

        graph @= remove_leading_zeros_fst
        self._fst = graph.optimize()


class AboveHundredFst(GraphFst):
    def __init__(self, case: str, gender: str, complement: str, cardinal_fst: GraphFst) -> None:
        
        prefix = self.build_prefix_graph(complement)

        complement_root = f"build_grammar/tagger/data/ordinal/{gender}/{case}/"
        complement_fst = pynini.string_file(complement_root + f"{complement}.tsv")

        process_only_complement = pynini.cross(complement_fst, "1")
        process_prefix_and_complement = prefix + pynutil.delete(complement_fst)

        ordinal_above_hundred_fst = pynini.union(process_only_complement, process_prefix_and_complement).optimize()

        if complement == "hundred":
            padding = "0"
        else:
            padding = "000"
        
        graph = pynini.union(
            ordinal_above_hundred_fst,
            cardinal_fst,
            pynutil.insert(padding)
        )

        self._fst = graph.optimize()

    def build_prefix_graph(self, complement: str):
        if complement == "hundred":
            prefix_root = "build_grammar/tagger/data/ordinal/prefixes/"
            return pynini.string_file(prefix_root + "hundred.tsv")
            
        prefix_root = "build_grammar/tagger/data/ordinal/prefixes/components/"
        digit_prefix_fst = pynini.string_file(prefix_root + "digit.tsv")
        teen_prefix_fst = pynini.string_file(prefix_root + "teen.tsv")
        ties_prefix_fst = pynini.string_file(prefix_root + "ties.tsv")
        hundred_prefix_fst = pynini.string_file(prefix_root + "hundred.tsv")

        up_to_thousand_prefix_fst = UpToThousandFst(digit_prefix_fst, teen_prefix_fst, ties_prefix_fst, hundred_prefix_fst).fst

        return pynini.union(up_to_thousand_prefix_fst)