from pynini.lib import pynutil
import pynini

def lstrip_class_label(label: str) -> pynini.Fst:
    """
    Strips the label from the start of a token.
    """
    return (
        pynutil.delete(f"{label}")
        + pynutil.delete(" { ")
    )

def rstrip_class_label() -> pynini.Fst:
    """
    Strips the label from the end of a token.
    """
    return (
        pynutil.delete(" } ")
    )