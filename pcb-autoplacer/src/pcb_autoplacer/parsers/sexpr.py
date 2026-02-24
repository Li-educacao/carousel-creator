"""Generic S-expression tokenizer and parser for KiCad files."""
from __future__ import annotations


def tokenize(text: str) -> list[str]:
    """Tokenize S-expression text into tokens: '(', ')', and atoms/strings.

    Handles nested parentheses, quoted strings with escape sequences, and
    line comments starting with ';' (not present in KiCad files but handled
    for robustness).
    """
    tokens: list[str] = []
    i = 0
    length = len(text)

    while i < length:
        ch = text[i]

        # Skip whitespace
        if ch in " \t\r\n":
            i += 1
            continue

        # Skip line comments
        if ch == ";":
            while i < length and text[i] != "\n":
                i += 1
            continue

        # Open paren
        if ch == "(":
            tokens.append("(")
            i += 1
            continue

        # Close paren
        if ch == ")":
            tokens.append(")")
            i += 1
            continue

        # Quoted string
        if ch == '"':
            i += 1  # skip opening quote
            buf: list[str] = []
            while i < length:
                c = text[i]
                if c == "\\":
                    # Escape sequence
                    i += 1
                    if i < length:
                        esc = text[i]
                        if esc == "n":
                            buf.append("\n")
                        elif esc == "t":
                            buf.append("\t")
                        elif esc == "r":
                            buf.append("\r")
                        else:
                            buf.append(esc)
                        i += 1
                elif c == '"':
                    i += 1  # skip closing quote
                    break
                else:
                    buf.append(c)
                    i += 1
            tokens.append('"' + "".join(buf) + '"')
            continue

        # Unquoted atom — read until whitespace, paren, or quote
        start = i
        while i < length and text[i] not in " \t\r\n()\";\\":
            i += 1
        atom = text[start:i]
        if atom:
            tokens.append(atom)

    return tokens


def parse(text: str) -> list:
    """Parse S-expression text into nested Python lists.

    The top-level expression is returned as a list (the outermost parens are
    stripped so '(a b (c d))' returns ['a', 'b', ['c', 'd']]).

    If the input contains multiple top-level expressions they are returned as
    a list of lists.
    """
    tokens = tokenize(text)
    pos = 0

    def parse_expr() -> list | str:
        nonlocal pos
        if tokens[pos] != "(":
            # Bare atom at top level — just return it
            atom = tokens[pos]
            pos += 1
            return atom
        pos += 1  # consume '('
        items: list = []
        while pos < len(tokens) and tokens[pos] != ")":
            if tokens[pos] == "(":
                items.append(parse_expr())
            else:
                token = tokens[pos]
                # Strip the sentinel quotes we added during tokenization
                if token.startswith('"') and token.endswith('"'):
                    items.append(token[1:-1])
                else:
                    items.append(token)
                pos += 1
        if pos < len(tokens):
            pos += 1  # consume ')'
        return items

    results: list = []
    while pos < len(tokens):
        results.append(parse_expr())

    if len(results) == 1:
        return results[0]
    return results


def find_nodes(tree: list, tag: str) -> list[list]:
    """Find all direct child nodes (sub-lists) whose first element equals tag.

    Example:
        find_nodes(['module', 'name', ['pad', '1'], ['pad', '2']], 'pad')
        → [['pad', '1'], ['pad', '2']]
    """
    result: list[list] = []
    for item in tree:
        if isinstance(item, list) and item and item[0] == tag:
            result.append(item)
    return result


def find_node(tree: list, tag: str) -> list | None:
    """Find the first direct child node with given tag, or None.

    Example:
        find_node(['comp', ['ref', 'R1'], ['value', '10k']], 'ref')
        → ['ref', 'R1']
    """
    for item in tree:
        if isinstance(item, list) and item and item[0] == tag:
            return item
    return None


def get_value(tree: list, tag: str, default: str = "") -> str:
    """Get the string value immediately after the tag in a child node.

    Example:
        get_value(['comp', ['ref', 'R1'], ['value', '10k']], 'ref') → 'R1'
        get_value(['comp', ['ref', 'R1']], 'missing') → ''
    """
    node = find_node(tree, tag)
    if node is None or len(node) < 2:
        return default
    val = node[1]
    if isinstance(val, str):
        return val
    return default
