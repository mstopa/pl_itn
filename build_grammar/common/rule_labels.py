from pynini.lib import pynutil
import pynini

def add_left_rule_label(label: str) -> pynini.Fst:
    """
    Adds the label to the start of a token.
    """
    return pynutil.insert(f"{label}: \"")

def add_right_rule_label() -> pynini.Fst:
    """
    Adds the label to the end of a token.
    """
    return pynutil.insert("\"")

def lstrip_rule_label(label: str) -> pynini.Fst:
    """
    Strips the label from the start of a token.
    """
    return (
        pynutil.delete(f"{label}:")
        + pynutil.delete(" \"")
    )

def rstrip_rule_label() -> pynini.Fst:
    """
    Strips the label from the end of a token.
    """
    return (
        pynutil.delete("\"")
    )