# tredge

[![pypi][pypi-img]][pypi-url]

[pypi-img]: https://img.shields.io/pypi/v/tredge?style=plastic
[pypi-url]: https://pypi.org/project/tredge/

This is tiny yet fast module to get set of explicitly defined transitive edges from a directed acyclic graph. Given a DAG with edges `child`<--`parent` represented as dictionary (keys are children, values are iterables with parents), or as iterable of iterables representing edges ((`child`, `parent`)), or as file object pointing to tab-delimited file with 2 columns (`child`, `parent`), it returns set of transitive edges found there. Original intent of this package was to use it for removing redundant edges from tree structures.

If a given graph is cyclic, `transitive_edges` function will not return edges that include vertices participating in loops. To find such vertices beforehand or make sure there are none, there is a function `cycles(g)`.

Usage:

```python
import tredge

g = {
    'b': {'a'},
    'c': {'a'},
    'd': {'b', 'c', 'a'},
    'e': {'d', 'a'}
}
result = tredge.transitive_edges(g)
print(result)

# {('d', 'a'), ('e', 'a')}
```

or

```python
import tredge

g = [
    ('b', 'a'),
    ('c', 'a'),
    ('d', 'b'),
    ('d', 'c'),
    ('e', 'd'),
    ('e', 'a'),
    ('d', 'a')
]
result = tredge.transitive_edges(g)
print(result)

# {('d', 'a'), ('e', 'a')}
```

or

```python
"""input_file.tab:
b	a
c	a
d	b
d	c
e	d
e	a
d	a
"""

import tredge

with open('input_file.tab', mode='r', encoding='utf8') as g:
    result = tredge.transitive_edges(g)
print(result)

# {('d', 'a'), ('e', 'a')}
```

To check if a graph has cycles:

```python
import tredge

g = {
    'b': {'a'},
    'c': {'a'},
    'd': {'b', 'c', 'a'},
    'e': {'d', 'a'}
}
result = tredge.cycles(g)
print(result)

# {'e', 'c', 'd'}
```
