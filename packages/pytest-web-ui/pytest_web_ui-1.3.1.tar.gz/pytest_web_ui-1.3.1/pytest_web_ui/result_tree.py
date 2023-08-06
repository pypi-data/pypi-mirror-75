"""
Defines a tree containing all PyTest test packages, modules, classes and
functions in their respective hierarchy. Used to render the test structure
in the UI and to update with test results as they are available.
"""

from __future__ import annotations
import abc
import enum
import textwrap
from typing import List, Tuple, Dict, Generator, Iterator, Optional, Any

import marshmallow
from marshmallow import fields
import marshmallow_enum  # type: ignore
from _pytest import nodes  # type: ignore

from pytest_web_ui import environment


class TestState(enum.Enum):
    """Possible states of a tree node."""

    INIT = "init"
    SKIPPED = "skipped"
    PASSED = "passed"
    FAILED = "failed"
    RUNNING = "running"


# A parent entry will inherit the highest precedence state from its children.
_TEST_STATE_PRECEDENT = {
    TestState.INIT: 1,
    TestState.SKIPPED: 2,
    TestState.PASSED: 3,
    TestState.FAILED: 4,
    TestState.RUNNING: 5,
}


def _status_precedent(statuses: Iterator[TestState]) -> TestState:
    """
    Return the status with the highest precedence. If the iterator is empty, INIT state
    is returned as a default.
    """
    return max(
        statuses,
        key=lambda status: _TEST_STATE_PRECEDENT[status],
        default=TestState.INIT,
    )


class Node(abc.ABC):
    """Define common interface for branch and leaf nodes."""

    def __init__(self):
        self.parent_ids: List[str] = []
        self._short_id = None

    @property
    @abc.abstractmethod
    def nodeid(self) -> str:
        """Return the unique ID for this node."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def short_id(self) -> str:
        """Return the short ID for this node."""
        raise NotImplementedError

    @property
    def status(self) -> TestState:
        """Property getter for current status."""
        return self._get_status()

    @status.setter
    def status(self, new_status: TestState):
        """"Property setter for current node status."""
        self._set_status(new_status)

    @abc.abstractmethod
    def _get_status(self) -> TestState:
        """Get the current status of this node."""
        raise NotImplementedError

    @abc.abstractmethod
    def _set_status(self, new_status: TestState):
        """Set the current status of this node."""
        raise NotImplementedError

    @abc.abstractmethod
    def pretty_format(self) -> str:
        """
        Format this node and its children recursively as a multi-line string, for debug
        purposes.
        """
        raise NotImplementedError


class BranchNode(Node):
    """
    A single branch node in the test tree. A branch node has at least one
    child - as such, this object represents a collection of testcases. The
    collection may be a test package, module or a class.
    """

    def __init__(
        self,
        nodeid: str,
        fspath: str,
        short_id: Optional[str] = None,
        env: Optional[environment.EnvironmentManager] = None,
    ):
        self._nodeid = nodeid
        self._fspath = fspath
        self._short_id = short_id
        self.child_branches: Dict[str, BranchNode] = {}
        self.child_leaves: Dict[str, LeafNode] = {}
        self.parent_ids: List[str] = []
        self.environment = env

    def __eq__(self, other: object) -> bool:
        """Compare two BranchNodes for equality."""
        if not isinstance(other, BranchNode):
            return False

        return self.nodeid == other.nodeid

    def __repr__(self) -> str:
        """String representation of this node."""
        return f"BranchNode <{self.nodeid} {self.status}>"

    def pretty_format(self) -> str:
        """Output a pretty-formatted string of the whole tree, for debug purposes."""
        formatted_children = textwrap.indent(
            "\n".join(child.pretty_format() for child in self.iter_children()),
            prefix="  ",
        )
        return f"{self}\n{formatted_children}"

    def iter_children(self) -> Generator[Node, None, None]:
        """Iterate over all child branches and leaves."""
        for branch in self.child_branches.values():
            yield branch
        for leaf in self.child_leaves.values():
            yield leaf

    @property
    def environment_state(self):
        if self.environment is None:
            return environment.EnvironmentState.INACTIVE

        return self.environment.state

    @property
    def nodeid(self) -> str:
        """Unique ID of this node, used for indexing."""
        return self._nodeid

    @property
    def short_id(self) -> str:
        """Short ID."""
        if self._short_id:
            return self._short_id
        return self.nodeid.split("::")[-1].split("/")[-1]

    @property
    def fspath(self) -> str:
        """Filesystem path this test node corresponds to."""
        return self._fspath

    def _get_status(self) -> TestState:
        """Return status of child entries."""
        return _status_precedent(child.status for child in self.iter_children())

    def _set_status(self, new_status: TestState):
        for child in self.iter_children():
            child.status = new_status


class LeafNode(Node):
    """
    A single leaf node in the test tree. A leaf node has no children and
    as such, represents a test function or method.
    """

    def __init__(self, item: nodes.Item):
        self._pytest_node = item
        self.report = None
        self._status = TestState.INIT
        self.parent_ids: List[str] = []

    def __eq__(self, other: object) -> bool:
        """Compare two LeafNodes for equality."""
        if not isinstance(other, LeafNode):
            return False

        return self.nodeid == other.nodeid

    def __repr__(self) -> str:
        """String representation of this node."""
        return f"LeafNode <{self._pytest_node} {self.status}>"

    @property
    def nodeid(self) -> str:
        return self._pytest_node.nodeid

    @property
    def short_id(self) -> str:
        """Short ID."""
        return self.nodeid.split("::")[-1]

    @property
    def longrepr(self) -> Optional[str]:
        if self.report is None or self.report.longrepr is None:
            return None

        return str(self.report.longrepr)

    def pretty_format(self) -> str:
        """Output a pretty-formatted string of the whole tree, for debug purposes."""
        return str(self)

    def _get_status(self) -> TestState:
        """
        Get the status of this entry. If there is a test report that means the test has
        run and we get the status from the report. Otherwise, the status may be either
        INIT (not yet run) or RUNNING (in progress of being run).
        """
        if self.report is None:
            return self._status
        return TestState(self.report.outcome)

    def _set_status(self, new_status):
        """
        Update the status. This is only called to either set this node as RUNNING or
        reset the state to INIT. In either case, we reset the test report to None if
        present.
        """
        if new_status not in (TestState.INIT, TestState.RUNNING):
            raise ValueError("Invalid state")
        self._status = new_status
        self.report = None


def build_from_session(
    session: nodes.Session, root_id: str
) -> Tuple[BranchNode, Dict[str, Node]]:
    """Build a result tree from the PyTest session object."""
    root = BranchNode(
        nodeid=session.nodeid, fspath=str(session.fspath), short_id=root_id
    )

    for item in session.items:
        collectors = item.listchain()[1:-1]
        branch = _ensure_branch(root, collectors)
        leaf = LeafNode(item)
        branch.child_leaves[leaf.short_id] = leaf

    pruned_tree = _prune_tree(root)
    if pruned_tree is None:
        raise RuntimeError("No tests were found")

    nodes_index = _build_index(pruned_tree)
    return pruned_tree, nodes_index


def _prune_tree(node: BranchNode) -> Optional[BranchNode]:
    """
    Recursively remove all branch nodes from the tree that only have a single child,
    instead directly linking to that child.
    """
    children = list(node.iter_children())
    if not children:
        return None
    if len(children) == 1 and isinstance(children[0], BranchNode):
        node = children[0]

    child_branches = {
        short_id: _prune_tree(child) for short_id, child in node.child_branches.items()
    }
    node.child_branches = {
        short_id: child
        for short_id, child in child_branches.items()
        if child is not None
    }
    return node


def _ensure_branch(node: BranchNode, collectors: List[nodes.Collector],) -> BranchNode:
    """
    Retrieve the branch node under the given root node that corresponds to the given
    chain of collectors. If any branch nodes do not yet exist, they will be
    automatically created.
    """
    # Base recursive case: return the current node if the list of collectors is empty.
    if not collectors:
        return node

    next_col, rest = collectors[0], collectors[1:]
    short_id = next_col.nodeid.split("::")[-1]

    try:
        child = node.child_branches[short_id]
    except KeyError:
        child = BranchNode(nodeid=next_col.nodeid, fspath=str(next_col.fspath))
        node.child_branches[short_id] = child

    return _ensure_branch(child, rest)


def set_parent_ids(node: BranchNode):
    """
    Recursively set the parent_ids attribute on this node and all of its
    children, based on the current tree structure.
    """
    for child_branch in node.child_branches.values():
        child_branch.parent_ids = node.parent_ids + [node.short_id]
        set_parent_ids(child_branch)

    for child_leaf in node.child_leaves.values():
        child_leaf.parent_ids = node.parent_ids + [node.short_id]


def _build_index(node: BranchNode) -> Dict[str, Node]:
    index: Dict[str, Node] = {node.nodeid: node}
    for child_leaf in node.child_leaves.values():
        index[child_leaf.nodeid] = child_leaf
    for child_branch in node.child_branches.values():
        index.update(_build_index(child_branch))

    return index


class NodeSchema(marshmallow.Schema):
    """Base schema for all nodes."""

    nodeid = fields.Str()
    short_id = fields.Str()
    status = marshmallow_enum.EnumField(TestState, by_value=True)


class LeafNodeSchema(NodeSchema):
    """Serialization schema for leaf nodes."""

    longrepr = fields.Str(allow_none=True)


class BranchNodeSchema(NodeSchema):
    """Serialization schema for branch nodes."""

    child_branches = fields.Dict(
        fields.Str(), fields.Nested(lambda: BranchNodeSchema())
    )
    child_leaves = fields.Dict(fields.Str(), fields.Nested(LeafNodeSchema()))
    environment_state = marshmallow_enum.EnumField(
        environment.EnvironmentState, by_value=True
    )


def serialize_parents_slice(
    result_node: Node, result_tree: BranchNode,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Serialize a slice of the tree from root to the given result node."""
    shallow_branch_schema = NodeSchema()
    serialized_root = shallow_branch_schema._serialize(result_tree)
    curr_serialized_node = serialized_root
    curr_node = result_tree

    for uid in result_node.parent_ids:
        curr_node = curr_node.child_branches[uid]
        serialized_child = shallow_branch_schema._serialize(curr_node)
        curr_serialized_node["child_branches"] = {uid: serialized_child}
        curr_serialized_node = serialized_child

    return serialized_root, curr_serialized_node
