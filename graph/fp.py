#! /usr/local/bin/python3
# builtin
import math
from collections import defaultdict, namedtuple
# custom
from util import log,logaz,mapl,memo,timit


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
# two-way node2nodes connection
def tuple2dict(graph):
  node2nodes = defaultdict(set)
  for k,v in sorted(graph):
    node2nodes[k].add(v)
    node2nodes[v].add(k)
  return node2nodes

# get node's group of nodes
@logaz('az')
def group(node):
  return [n for n,root in node2root.items() if root==node]

@logaz('z')
def uniq(*itr): return set(*itr)

@logaz('z')
def show_groups():
  root2nodes = defaultdict(set)
  for n,r in node2root.items():
    root2nodes[r].add(n)
  return root2nodes
# explore from each goal-group; merge other groups on contact
@logaz('az')
def expand(goal): # -> root for goal-group
  @logaz('az')
  def explore(goal):
    group = uniq(node for node,root in node2root.items() if root==goal)
    nexts = set.union(*[node2nodes[node] for node in group]) - group
    return nexts
  @logaz('az')
  def merge(*nodes):
    # TODO inform respective roots of mutual best dist
    n2r = node2root
    root_min = min(n2r[n] for n in nodes)
    for n in nodes:
      n2r[n] = root_min
    return root_min
  root_new = merge(goal,*explore(goal))
  show_groups()
  return root_new

# simultaneous BFS from all goals until coalesce into one group
def coalesce(goals):
  def terminal(goals):
    return len(goals)==1
  def step(i=-1):
    i+=1
    if i: log(i)
    return i
  i = step()
  while not terminal(goals): # goals_curr
    i = step(i)
    goals = uniq(mapl(expand, goals)) # goals_next
  log('fini @ %s',i)


node2nodes = tuple2dict(tuple_graph) # graph
node2root = {n:n for n in node2nodes} # groups
# node2node2dist = defaultdict(dict) # node -> node -> dist
# info = namedtuple('Info','n2ns,n2r,n2n2d')(node2nodes,node2root,node2node2dist)
goals = (2,5,8)
coalesce(goals)


