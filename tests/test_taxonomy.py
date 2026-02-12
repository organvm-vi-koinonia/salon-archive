"""Tests for the taxonomy module."""
from src.taxonomy import Taxonomy, TaxonomyNode


def test_add_and_retrieve_node():
    tax = Taxonomy()
    tax.add_node(TaxonomyNode(slug="philosophy", label="Philosophy"))
    node = tax.get_node("philosophy")
    assert node.label == "Philosophy"

def test_parent_child_relationship():
    tax = Taxonomy()
    tax.add_node(TaxonomyNode(slug="art", label="Art"))
    tax.add_node(TaxonomyNode(slug="generative", label="Generative Art", parent_slug="art"))
    parent = tax.get_node("art")
    assert len(parent.children) == 1

def test_get_roots():
    tax = Taxonomy()
    tax.add_node(TaxonomyNode(slug="a", label="A"))
    tax.add_node(TaxonomyNode(slug="b", label="B", parent_slug="a"))
    roots = tax.get_roots()
    assert len(roots) == 1
    assert roots[0].slug == "a"

def test_search_nodes():
    tax = Taxonomy()
    tax.add_node(TaxonomyNode(slug="recursion", label="Recursive Systems", description="Self-referential"))
    results = tax.search("recursive")
    assert len(results) == 1
