"""Taxonomy module for categorizing and tagging salon content.

DEPRECATED: This in-memory implementation is retained as an offline fallback.
For database-backed operations, use repository.py with koinonia-db models.

Manages a hierarchical taxonomy of topics, themes, and concepts
used to organize salon sessions and enable cross-session discovery.
"""

from __future__ import annotations

import warnings

warnings.warn(
    "salon_archive.taxonomy is deprecated — use repository.SalonRepository instead",
    DeprecationWarning,
    stacklevel=2,
)

from dataclasses import dataclass, field  # noqa: E402
from typing import Any  # noqa: E402


@dataclass
class TaxonomyNode:
    """A node in the topic taxonomy tree."""
    slug: str
    label: str
    parent_slug: str | None = None
    children: list[TaxonomyNode] = field(default_factory=list)
    description: str = ""

    def add_child(self, child: TaxonomyNode) -> None:
        child.parent_slug = self.slug
        self.children.append(child)

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "slug": self.slug,
            "label": self.label,
            "parent": self.parent_slug,
            "children": [c.slug for c in self.children],
        }


class Taxonomy:
    """Hierarchical topic taxonomy for salon content organization."""

    def __init__(self) -> None:
        self._nodes: dict[str, TaxonomyNode] = {}

    def add_node(self, node: TaxonomyNode) -> None:
        if node.slug in self._nodes:
            raise ValueError(f"Taxonomy node '{node.slug}' already exists")
        self._nodes[node.slug] = node
        if node.parent_slug and node.parent_slug in self._nodes:
            self._nodes[node.parent_slug].add_child(node)

    def get_node(self, slug: str) -> TaxonomyNode:
        return self._nodes[slug]

    def get_roots(self) -> list[TaxonomyNode]:
        return [n for n in self._nodes.values() if n.parent_slug is None]

    def get_descendants(self, slug: str) -> list[TaxonomyNode]:
        result: list[TaxonomyNode] = []
        node = self._nodes.get(slug)
        if not node:
            return result
        stack = list(node.children)
        while stack:
            current = stack.pop()
            result.append(current)
            stack.extend(current.children)
        return result

    def search(self, query: str) -> list[TaxonomyNode]:
        q = query.lower()
        return [n for n in self._nodes.values() if q in n.label.lower() or q in n.description.lower()]

    @property
    def total_nodes(self) -> int:
        return len(self._nodes)
