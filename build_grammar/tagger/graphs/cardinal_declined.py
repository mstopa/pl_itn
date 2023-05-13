import pynini
from pynini.lib import pynutil

from common.graph import GraphFst, accept_space_fst, maybe_delete_space_fst, non_zero_number, surely_delete_space_fst
from common.rule_labels import add_left_rule_label, add_right_rule_label
from common.class_labels import add_left_class_label, add_right_class_label

from tagger.graphs.sign import SignFst
from tagger.graphs.cardinal_common import UpToThousandFst, remove_leading_zeros_fst
from tagger.graphs.cardinal_basic import AboveThousandFst as CardinalBasicAboveThousandFst


class CardinalDeclinedFst(GraphFst):
    def __init__(self, cardinal_basic_fst: pynini.Fst):

        graph = pynini.string_file("build_grammar/tagger/data/cardinal_declined/zero.tsv")

        for gender in ("fem",  "m1",  "m2",  "m3",  "n1",  "n2",  "p1",  "p2"):
            for case in ("nom", "gen", "dat", "acc", "inst", "loc"):
                graph |= GenderCaseCardinalFst(gender, case, cardinal_basic_fst).fst

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

        self.fst = transformation.optimize()


class GenderCaseCardinalFst(GraphFst):
    def __init__(self, gender: str, case: str, cardinal_basic_fst: pynini.Fst):
        root = f"build_grammar/tagger/data/cardinal_declined/{gender}/{case}/"
        unit_fst = pynini.string_file(root + "digit.tsv")
        teen_fst = pynini.string_file(root + "teen.tsv")
        ties_fst = pynini.string_file(root + "ties.tsv")
        hundred_fst = pynini.string_file(root + "hundred.tsv")

        up_to_thousand_fst = UpToThousandFst(unit_fst, teen_fst, ties_fst, hundred_fst).fst
        non_zero_up_to_thousand_number = up_to_thousand_fst @ non_zero_number

        above_thousand_fst = AboveThousandFst(
            gender, 
            case, 
            "thousand", 
            cardinal_basic_fst.above_thousand_fst,
            non_zero_up_to_thousand_number
        ).fst
        above_million_fst = AboveThousandFst(
            gender,
            case,
            "million",
            cardinal_basic_fst.above_million_fst,
            non_zero_up_to_thousand_number
        ).fst
        above_billion_fst = AboveThousandFst(
            gender,
            case,
            "billion",
            cardinal_basic_fst.above_billion_fst,
            non_zero_up_to_thousand_number
        ).fst

        graph = (
            above_billion_fst
            + maybe_delete_space_fst
            + above_million_fst
            + maybe_delete_space_fst
            + above_thousand_fst
            + maybe_delete_space_fst
            + up_to_thousand_fst
        )

        graph @= remove_leading_zeros_fst
        self.fst = graph.optimize()


class AboveThousandFst(GraphFst):
    def __init__(self, gender: str, case: str, complement: str, cardinal_basic_fst: pynini.Fst, non_zero_up_to_thousand_number: pynini.Fst):
        if case == "nom":
            self.fst = cardinal_basic_fst
            return
        
        sg_complement_fst = pynini.string_file(f"build_grammar/tagger/data/cardinal_declined/{gender}/{case}/{complement}_sg.tsv")
        pl_complement_fst = pynini.string_file(f"build_grammar/tagger/data/cardinal_declined/{gender}/{case}/{complement}_pl.tsv")

        # for example "tysiąca"
        sg_transformation = pynini.cross(sg_complement_fst, "001")

        # for example "dwóm tysiącom"
        pl_transformation = pynini.union(
            non_zero_up_to_thousand_number
            + surely_delete_space_fst
            + pynutil.delete(pl_complement_fst)
        )

        self.fst = pynini.union(
            sg_transformation,
            pl_transformation,
            pynutil.insert("000")
        )