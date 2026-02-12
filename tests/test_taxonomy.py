"""Tests for the taxonomy module."""

import pytest

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


# --- Expanded tests for PRODUCTION promotion ---


def test_duplicate_slug_raises():
    tax = Taxonomy()
    tax.add_node(TaxonomyNode(slug="art", label="Art"))
    with pytest.raises(ValueError, match="already exists"):
        tax.add_node(TaxonomyNode(slug="art", label="Art Duplicate"))


def test_total_nodes():
    tax = Taxonomy()
    assert tax.total_nodes == 0
    tax.add_node(TaxonomyNode(slug="a", label="A"))
    tax.add_node(TaxonomyNode(slug="b", label="B"))
    assert tax.total_nodes == 2


def test_is_leaf():
    parent = TaxonomyNode(slug="parent", label="Parent")
    child = TaxonomyNode(slug="child", label="Child")
    assert parent.is_leaf is True
    parent.add_child(child)
    assert parent.is_leaf is False
    assert child.is_leaf is True


def test_to_dict():
    node = TaxonomyNode(slug="test", label="Test Node", parent_slug="root")
    d = node.to_dict()
    assert d["slug"] == "test"
    assert d["label"] == "Test Node"
    assert d["parent"] == "root"
    assert d["children"] == []


def test_get_descendants():
    tax = Taxonomy()
    tax.add_node(TaxonomyNode(slug="root", label="Root"))
    tax.add_node(TaxonomyNode(slug="child", label="Child", parent_slug="root"))
    tax.add_node(TaxonomyNode(slug="grandchild", label="Grandchild", parent_slug="child"))
    descendants = tax.get_descendants("root")
    slugs = {d.slug for d in descendants}
    assert "child" in slugs
    assert "grandchild" in slugs
    assert len(descendants) == 2


def test_get_descendants_empty():
    tax = Taxonomy()
    tax.add_node(TaxonomyNode(slug="leaf", label="Leaf"))
    assert tax.get_descendants("leaf") == []


def test_get_descendants_missing_slug():
    tax = Taxonomy()
    assert tax.get_descendants("nonexistent") == []


def test_search_by_description():
    tax = Taxonomy()
    tax.add_node(TaxonomyNode(slug="onto", label="Ontology", description="Study of being and existence"))
    results = tax.search("existence")
    assert len(results) == 1
    assert results[0].slug == "onto"


def test_search_no_results():
    tax = Taxonomy()
    tax.add_node(TaxonomyNode(slug="art", label="Art"))
    results = tax.search("zzz_nonexistent_zzz")
    assert len(results) == 0
