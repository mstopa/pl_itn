import pynini

from pl_itn.src.utils import draw_graph

def tag(tagger_fst, text):
    text = pynini.escape(text)

    lattice = text @ tagger_fst
    draw_graph(lattice, "Tagger lattice", "tagger.dot")

    text = pynini.shortestpath(lattice, nshortest=1, unique=True).string()

    if text is None:
        raise ValueError("Tagger returned no output.")
    return text
