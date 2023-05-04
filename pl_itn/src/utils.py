import re
from string import punctuation

import pynini

def pre_process(text: str):
    text = text.lower()
    text = _surround_punctuation_with_spaces(text)
    text = _remove_multiple_whitespaces(text)
    return text

def post_process(text: str):
    text = _remove_multiple_whitespaces(text)
    return text

def _surround_punctuation_with_spaces(text: str):
    for punct in punctuation:
        text = text.replace(punct, f" {punct} ")
    return text

def _remove_multiple_whitespaces(text: str):
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text

utf_symbols = [
    ("<eps>", 0), ("<space>", 32), ("!", 33), ('"', 34), ("#", 35), 
    ("$", 36), ("%", 37), ("&", 38), ("'", 39), ("(", 40), (")", 41), 
    ("*", 42), ("+", 43), (",", 44), ("-", 45), (".", 46), ("/", 47), 
    ("0", 48), ("1", 49), ("2", 50), ("3", 51), ("4", 52), ("5", 53), 
    ("6", 54), ("7", 55), ("8", 56), ("9", 57), (":", 58), (";", 59), 
    ("<", 60), ("=", 61), (">", 62), ("?", 63), ("@", 64), ("A", 65), 
    ("B", 66), ("C", 67), ("D", 68), ("E", 69), ("F", 70), ("G", 71), 
    ("H", 72), ("I", 73), ("J", 74), ("K", 75), ("L", 76), ("M", 77), 
    ("N", 78), ("O", 79), ("P", 80), ("Q", 81), ("R", 82), ("S", 83), 
    ("T", 84), ("U", 85), ("V", 86), ("W", 87), ("X", 88), ("Y", 89), 
    ("Z", 90), ("[", 91), ("\\", 92), ("]", 93), ("^", 94), ("_", 95), 
    ("`", 96), ("a", 97), ("b", 98), ("c", 99), ("d", 100), ("e", 101), 
    ("f", 102), ("g", 103), ("h", 104), ("i", 105), ("j", 106), ("k", 107), 
    ("l", 108), ("m", 109), ("n", 110), ("o", 111), ("p", 112), ("q", 113), 
    ("r", 114), ("s", 115), ("t", 116), ("u", 117), ("v", 118), ("w", 119), 
    ("x", 120), ("y", 121), ("z", 122), ("{", 123), ("|", 124), ("}", 125), 
    ("~", 126), ("X",  127)
]

def draw_graph(lattice: pynini.Fst, title: str, path: str = "graph.dot"):
    isymbols = pynini.SymbolTable()
    for symbol, code in utf_symbols:
        isymbols.add_symbol(symbol, code)
    
    lattice.draw(
        path, 
        isymbols=isymbols, osymbols=isymbols, 
        acceptor=True, title=title, portrait=True)

    # dot -Tps tagger.dot >tagger.ps