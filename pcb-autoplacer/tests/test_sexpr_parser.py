"""Tests for the S-expression parser."""
from pcb_autoplacer.parsers.sexpr import tokenize, parse, find_nodes, find_node, get_value


class TestTokenize:
    def test_simple(self):
        tokens = tokenize("(a b c)")
        assert tokens == ["(", "a", "b", "c", ")"]

    def test_nested(self):
        tokens = tokenize("(a (b c))")
        assert tokens == ["(", "a", "(", "b", "c", ")", ")"]

    def test_quoted_string(self):
        tokens = tokenize('(a "hello world")')
        assert tokens == ["(", "a", '"hello world"', ")"]

    def test_numbers(self):
        tokens = tokenize("(at 1.5 -2.3)")
        assert tokens == ["(", "at", "1.5", "-2.3", ")"]


class TestParse:
    def test_simple(self):
        result = parse("(a b c)")
        assert result == ["a", "b", "c"]

    def test_nested(self):
        result = parse("(a (b c) (d e))")
        assert result == ["a", ["b", "c"], ["d", "e"]]

    def test_quoted(self):
        result = parse('(name "hello world")')
        assert result == ["name", "hello world"]

    def test_deep_nesting(self):
        result = parse("(a (b (c d)))")
        assert result == ["a", ["b", ["c", "d"]]]


class TestFindNodes:
    def test_find_multiple(self):
        tree = ["module", "name", ["pad", "1"], ["pad", "2"], ["at", "0", "0"]]
        pads = find_nodes(tree, "pad")
        assert len(pads) == 2
        assert pads[0] == ["pad", "1"]
        assert pads[1] == ["pad", "2"]

    def test_find_none(self):
        tree = ["module", "name"]
        result = find_nodes(tree, "pad")
        assert result == []


class TestFindNode:
    def test_found(self):
        tree = ["comp", ["ref", "R1"], ["value", "10k"]]
        node = find_node(tree, "ref")
        assert node == ["ref", "R1"]

    def test_not_found(self):
        tree = ["comp", ["ref", "R1"]]
        assert find_node(tree, "missing") is None


class TestGetValue:
    def test_found(self):
        tree = ["comp", ["ref", "R1"], ["value", "10k"]]
        assert get_value(tree, "ref") == "R1"
        assert get_value(tree, "value") == "10k"

    def test_default(self):
        tree = ["comp", ["ref", "R1"]]
        assert get_value(tree, "missing") == ""
        assert get_value(tree, "missing", "N/A") == "N/A"
