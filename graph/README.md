# graph `{explore}`

find minimal traversal linking nodes in graph

1. [steps.ipynb](steps.ipynb)

    > Jupyter Notebook illustrating a few iterations of oop.py


1. [fp.py](fp.py)

    > functional style: "flatter" data-structure & flow but possibly harder to reason about


1. [oop.py](oop.py)

    > object-oriented style: requires more work representing different elements & abstraction levels but aids later operations e.g. explore, merge

## log & term convention
- `root`: for identifying a Group, always using minimum-ID among constituent Nodes
- `4<2`: shorthand Node(4) in group rooted @ Node(2)
- `Node-11<1: [6,14]`: full-notation Node(11) in group rooted @ Node(1) & connected to Nodes[6,14]
- `Group @ 1: [1<1,2<1,3<1,4<1]`: Group rooted @ Node(1) comprising Nodes[1,2,3,4]


## TODO
- consider distance-bounds
- stabilize networkx plots
- gen rand graph via networkx

