#! /usr/local/bin/python3
# builtin
import math, random
from collections import defaultdict, namedtuple
# custom
from util import get_logger,log,logaz,mapl,memo,timit


# dist_unknown = lambda:math.inf
# nodes2dist = defaultdict(dist_unknown) # (id,id) -> dist

# memoize Node to single-creation & retrieval
@memo() # id Node by Node.id
class Node:
  def __init__(self,_id):
    self.id = _id
    self.root = self # unique group-root
    self.edges = []
    # log(repr(self))
  def conn(self, node): # undirected graph
    assert isinstance(node,__class__)
    self.edges.append(node)
    node.edges.append(self)
  def reroot(self, root_new): # path-compression !
    if (self.root!=self # self not group.root
      and self.root!=root_new # group.root changed
      ): # propagate reroot to parent-Node
      Node(self.root).reroot(root_new)
    self.root = root_new
  def __str__(self): # 'self<root'
    # return str(self.id)
    return '%s<%s'%(self.id, self.root.id)
  def __repr__(self):
    edge_ids = '[%s]'%(','.join(map(str,[e.id for e in self.edges])))
    return '%s-%s<%s: %s'%(self.__class__.__name__, self.id, self.root.id, edge_ids)
  def __hash__(self):
    return self.id
  def __eq__(self, other):
    return hash(self)==hash(other)
  def __lt__(self, other):
    return self.id < other.id
@memo() # id Group by Group.root
class Group:
  def __init__(self,root:Node):
    self.nodes = {root} # no nodes implies singleton Group
    # log(repr(self))
  def add(self, nodes): # add Nodes, update everyone's root & Group
    root_prev = self.root
    self.nodes |= set(nodes)
    root_next = self.root
    # another Group dominates self -> merge groups
    if root_prev > root_next: 
      self = Group(root_next).add(self.nodes)
    # self dominates -> reroot Nodes & absorb any Group in which these Nodes belong
    elif nodes:
      nodes = set.union(*[Group(node.root).nodes for node in nodes])
      self.nodes |= nodes
      for node in nodes:
        node.reroot(root_next)
    return self
  @property
  def root(self):
    return min([node.root for node in self.nodes], key=lambda node:node.id)
  @property
  def id(self):
    return self.root.id
  @property
  @logaz('az')
  def neighbors(self):
    nodes_ngbr = set.union(*[set(node.edges) for node in self.nodes])
    nodes_outer = nodes_ngbr - self.nodes
    return nodes_outer
  # breadth-first-search -> absorb next layer of Nodes into Group
  @logaz('z')
  def bfs(self):
    return self.add(self.neighbors)
  def __lt__(self, other):
    return self.root < other.root
  def __repr__(self):
    str_nodes = '[%s]'%(','.join(mapl(str, self.nodes)))
    return '%s @ %s: %s'%(self.__class__.__name__, self.id, str_nodes)
  def __hash__(self): # crucial in recognizing group-merge
    return self.root.id
  def __eq__(self, other): # crucial in recognizing group-merge
    return hash(self)==hash(other)

# translate graph: edge-tuples -> Nodes
def tuple_graph2nodes(tuple_graph):
  nodes = set()
  for id0, id1 in tuple_graph:
    n0, n1 = Node(id0), Node(id1)
    nodes.add(n0)
    nodes.add(n1)
    n0.conn(n1)
  return nodes

# all Groups expand 1 hop
@logaz('z')
def explore(goal_groups):
  groups_visited = set()
  for group in goal_groups:
    if group not in groups_visited:
      groups_visited.add(group.bfs())
    else:
      log('%s already considered!', group)
  # continue using possibly-shrunken set of goal-groups
  return groups_visited

# random-pick goals for testing
@logaz('z')
def rand_pick_goals(nodes,k=3):
  return sorted(random.sample(nodes,k=k))

def terminal(goal_groups):
  return len(goal_groups)<=1


if __name__=='__main__':
  """ starts simple but extendable
    strongly-connected
    undirected
    unweighted
    static
    """
  tuple_graph = [
    (1,2),
    (1,12),
    (2,3),
    (2,4),
    (3,9),
    (3,10),
    (4,5),
    (4,7),
    (4,10),
    (5,6),
    (5,12),
    (6,11),
    (7,8),
    ]
  # TODO randgen graph via networkx

  nodes = tuple_graph2nodes(tuple_graph)
  # goals = rand_pick_goals(nodes)
  goals = mapl(Node, (8,9,11))
  # goals = mapl(Node, (8,11))
  goal_groups = [Group(goal) for goal in goals]

  # simultaneous BFS from all goals until coalesce into one group
  i = 0
  while not terminal(goal_groups):
    i+=1
    log(i)
    goal_groups = explore(goal_groups)

