Parse Grammar
=============

A library containing Directed Graph representing symbol to symbol translation with a Grammar class representing a start symbol and any terminal symbols.

Used for representing finite state machines in automation bots.

Usage
=====

`import grammar as gram`

`pGraph = gram.Graph()`

`pGrammar = gram.Grammar(<start_symbol>, <end_symbol>, pGraph)`

where <start_symbol> is a vertex within pGraph
where <end_symbol> is a vertex, or list/set of verticies, within pGraph

The <start_symbol> can not be an isolated vertex.
