import pynini
from pynini.lib import pynutil

from common.graph import GraphFst, maybe_delete_space_fst, surely_delete_space_fst, accept_space_fst, digit_fst, non_zero_number
from common.rule_labels import add_left_rule_label, add_right_rule_label
from common.class_labels import add_left_class_label, add_right_class_label

from tagger.graphs.sign import SignFst
from tagger.graphs.cardinal_common import UpToThousandFst, remove_leading_zeros_fst


class CardinalBasicFst(GraphFst):
    def __init__(self):
        zero_fst = pynini.string_file("build_grammar/tagger/data/cardinal_basic/zero.tsv")
        unit_fst = pynini.string_file("build_grammar/tagger/data/cardinal_basic/digit.tsv")
        teen_fst = pynini.string_file("build_grammar/tagger/data/cardinal_basic/teen.tsv")
        ties_fst = pynini.string_file("build_grammar/tagger/data/cardinal_basic/ties.tsv")
        hundred_fst = pynini.string_file("build_grammar/tagger/data/cardinal_basic/hundred.tsv")

        up_to_thousand_fst = UpToThousandFst(unit_fst, teen_fst, ties_fst, hundred_fst).fst
        
        above_thousand_fst = AboveThousandFst("tysiąc", "tysiące", "tysięcy", up_to_thousand_fst).fst
        above_million_fst = AboveThousandFst("milion", "miliony", "milionów", up_to_thousand_fst).fst
        above_billion_fst = AboveThousandFst("miliard", "miliardy", "miliardów", up_to_thousand_fst).fst

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

        graph |= zero_fst

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

        # export to reuse in cardinal_declined:
        self.above_thousand_fst = above_thousand_fst
        self.above_million_fst = above_million_fst
        self.above_billion_fst = above_billion_fst
        

class AboveThousandFst(GraphFst):
    def __init__(self, sg_nominative_complement: str, pl_nominative_complement, pl_genitive_complement: str, up_to_thousand_fst) -> None:
        # This graph transforms numbers above thousand, for example `sto dwadzieścia pięć tysięcy` or `trzy miliony`
        # In order to enter this path there are two components required: a non_zero_up_to_thousand_number and the complementing part
        # The complementing part is either sg_nominative, pl_nominative of pl_genitive depending on the number
        non_zero_up_to_thousand_number = up_to_thousand_fst @ non_zero_number

        # Numbers ended with digits 2, 3 or 4 are complemented by pl_nominatives, for example `dwa tysiące`
        numbers_complemented_by_pl_nominative = pynini.closure(digit_fst) + pynini.union("2", "3", "4")
        # With the exception for teens: 12, 13, 14. These are complemented by genitive, for example `dwanaście tysięcy`
        numbers_complemented_by_pl_nominative -= pynini.union("012", "013", "014")
        # Exclude bare zero from this path
        numbers_complemented_by_pl_nominative -= "000"
        number_fst = non_zero_up_to_thousand_number @ numbers_complemented_by_pl_nominative
        pl_nominative_fst = number_fst + surely_delete_space_fst + pynutil.delete(pl_nominative_complement)

        # Numbers ended with digits above 4 are complemented by genitive, for example `pięć tysięcy`
        numbers_complemented_by_pl_genitive = pynini.closure(digit_fst) + pynini.union("5", "6", "7", "8", "9")
        # Add exceptional teens which are complemented by genitive, for example `dwanaście tysięcy`
        numbers_complemented_by_pl_genitive += pynini.union("011", "012", "013", "014")
        number_fst = non_zero_up_to_thousand_number @ numbers_complemented_by_pl_genitive
        pl_genitive_fst = number_fst + surely_delete_space_fst + pynutil.delete(pl_genitive_complement)

        # But it is also possible to skip the numeral, for example 'tysiąc' -> 1000
        sg_nominative_fst = pynini.cross(sg_nominative_complement, "001")

        self._fst = pynini.union(
            sg_nominative_fst,
            pl_nominative_fst,
            pl_genitive_fst,
            pynutil.insert("000")
        )