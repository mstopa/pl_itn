import pynini
from pynini.lib import pynutil

from common.graph import GraphFst
from common.rule_labels import add_left_rule_label, add_right_rule_label
from common.class_labels import add_left_class_label, add_right_class_label


class CardinalBasicFst(GraphFst):
    def __init__(self):
        zero_fst = pynini.string_file("build_grammar/tagger/data/cardinal_basic/zero.tsv")
        digit_fst = pynini.string_file("build_grammar/tagger/data/cardinal_basic/digit.tsv")
        ties_fst = pynini.string_file("build_grammar/tagger/data/cardinal_basic/ties.tsv")
        teen_fst = pynini.string_file("build_grammar/tagger/data/cardinal_basic/teen.tsv")
        hundred_fst = pynini.string_file("build_grammar/tagger/data/cardinal_basic/hundred.tsv")

        graph = zero_fst

        transformation = (
            add_left_rule_label("integer")
            + graph
            + add_right_rule_label()
        )

        transformation = (
            add_left_class_label("cardinal")
            + transformation
            + add_right_class_label()
        )  

        self._fst = transformation.optimize()

    #     graph_hundred_and_below_component = self.compose_hundred_and_below_component()
    #     graph_hundred_and_below_component_at_least_one_none_zero_digit = (
    #         self.compose_hundred_and_below_component_at_least_one_none_zero_digit()
    #     )
    #     # shortcut attribute to be used in helper methods called below
    #     self.nonzero_hundred = graph_hundred_and_below_component_at_least_one_none_zero_digit.optimize()

    #     graph_thousand_component = self.compose_thousand_component()
    #     graph_million_component = self.compose_million_component()
    #     graph_billion_component = self.compose_billion_component()

    #     graph_remove_leading_zeros = (
    #         pynutil.delete(pynini.closure("0"))
    #         + pynini.difference(DIGIT, "0")
    #         + pynini.closure(DIGIT)
    #     )

    #     graph = (
    #         graph_billion_component  # leading 0 or billion conversion if detected
    #         + delete_space
    #         + graph_million_component  # leading 0 or million conversion if detected
    #         + delete_space
    #         + graph_thousand_component  # leading 0 or thousand conversion if detected
    #         + delete_space
    #         + graph_hundred_and_below_component  # leading 0 or hundred and anything below
    #         # conversion if detected
    #     ) @ graph_remove_leading_zeros

    #     graph |= self.graph_zero
    #     self.graph = graph  # to be used by other classes
    #     labeled_graph = add_rule_label(graph, "integer")

    #     optional_minus_graph = self.compose_optional_minus_graph()

    #     final_graph = (
    #         optional_minus_graph
    #         + accept_space
    #         + labeled_graph
    #     )
    #     final_graph = self.add_tokens(final_graph)

    #     # other fields for other classes to use
    #     self.fst = final_graph.optimize()
    #     self.graph = graph.optimize()
    #     self.graph_thousand = graph_thousand_component.optimize()
    #     self.graph_million = graph_million_component.optimize()
    #     self.graph_billion = graph_billion_component.optimize()

    # def compose_optional_minus_graph(self):
    #     graph = pynini.cross("minus", "\"-\"")
    #     labeled_graph = pynutil.insert("negative: ") + graph
    #     optional_labeled_graph = pynini.closure(
    #         labeled_graph,
    #         0, 1
    #     )
    #     return optional_labeled_graph

    # def compose_hundred_and_below_component(self):
    #     """
    #     Possible options:
    #     001 <- [hundred: 0][ties: 0 teens: 0][units: 1]
    #     011 <- [hundred: 0][ties: 0 teens: 1][units: 0]
    #     021 <- [hundred: 0][ties: 1 teens: 0][units: 1]
    #     101 <- [hundred: 1][ties: 0 teens: 0][units: 1]
    #     111 <- [hundred: 1][ties: 0 teens: 1][units: 0]
    #     121 <- [hundred: 1][ties: 1 teens: 0][units: 1]
    #     """
    #     graph = pynini.union(
    #         self.graph_hundred,
    #         pynutil.insert("0")
    #     )

    #     graph += delete_space
    #     graph += pynini.union(
    #         (self.graph_teen | pynutil.insert("00")),
    #         (self.graph_ties | pynutil.insert("0")) +
    #         delete_space + (self.graph_digit | pynutil.insert("0"))
    #     )
    #     return graph

    # def compose_hundred_and_below_component_at_least_one_none_zero_digit(self):
    #     hundred_component = self.compose_hundred_and_below_component()
    #     graph_at_least_one_none_zero_digit = (
    #         pynini.closure(DIGIT)
    #         + (pynini.union(DIGIT) - "0")
    #         + pynini.closure(DIGIT)
    #     )
    #     return (
    #         hundred_component
    #         @ graph_at_least_one_none_zero_digit
    #     )

    # def compose_complex_component(self, single_unit_complement, nominative_complement, genitive_complement):
    #     # Single unit, for example `tysiąc`
    #     nonzero_hundred_single_unit = '001'
    #     graph_single_unit = pynini.cross(single_unit_complement, nonzero_hundred_single_unit)

    #     # Numerals ended with digits 2, 3 or 4 are complemented by nominatives, for example `dwa tysiące`
    #     numbers_complemented_by_nominative = (
    #         pynini.closure(DIGIT) + pynini.union("2", "3", "4")
    #     )
    #     # teens are always complemented by genitive
    #     numbers_complemented_by_nominative -= (
    #         pynini.closure(DIGIT) + "1" + DIGIT)

    #     nonzero_hundred_complemented_by_nominative = self.nonzero_hundred @ numbers_complemented_by_nominative
    #     graph_complemented_by_nominative = (
    #         nonzero_hundred_complemented_by_nominative
    #         + delete_space
    #         + pynutil.delete(nominative_complement)
    #     )

    #     # Numerals ended with digits above 4 are complemented by genitive, for example `pięć tysięcy`
    #     numbers_complemented_by_genitive = (
    #         pynini.closure(DIGIT)
    #         - pynini.union(
    #             nonzero_hundred_single_unit,
    #             numbers_complemented_by_nominative
    #         )
    #     )
    #     nonzero_hundred_complemented_by_genitive = self.nonzero_hundred @ numbers_complemented_by_genitive
    #     graph_complemented_by_genitive = (
    #         nonzero_hundred_complemented_by_genitive
    #         + delete_space
    #         + pynutil.delete(genitive_complement)
    #     )

    #     return pynini.union(
    #         graph_single_unit,
    #         graph_complemented_by_nominative,
    #         graph_complemented_by_genitive,
    #         pynutil.insert("000")
    #     )

    # def compose_thousand_component(self):
    #     return self.compose_complex_component(
    #         "tysiąc", "tysiące", "tysięcy"
    #     )

    # def compose_million_component(self):
    #     return self.compose_complex_component(
    #         "milion", "miliony", "milionów"
    #     )

    # def compose_billion_component(self):
    #     return self.compose_complex_component(
    #         "miliard", "miliardy", "miliardów"
    #     )