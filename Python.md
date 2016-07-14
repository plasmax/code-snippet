# Python Code Snippet

## Formating

### Use variable name to format strings

```python
prefix = "HAHA"
attr = "HOHO"
print "{prefix}{attr}".format(**locals())
```

In python 3+ you can do this simply with:

```python
prefix = "HAHA"
attr = "HOHO"
print f"{prefix}{attr}"
```

## Iterator

Here is a list of useful [iterators](http://pymbook.readthedocs.io/en/latest/igd.html) not present in the [itertools](https://docs.python.org/2/library/itertools.html) module.

### Iterate over packets of N elements in the given list

This is useful for frame range generation when creating renderfarm jobs (eg: RIB genration).

Pattern is:`ABCDEF` -> `AB, CD, EF`

```python
def chunck(l, n):
    return (l[i:i+n] for i in xrange(0, len(l), n))
```

```python
>>> list(chunck(range(16),3))
[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15]]
```

### Pair sliding

Usefull to organize a list of connected nodes inside a graph.

Pattern is:`ABCDEF` -> `AB, BC, CD, DE, EF`

```python
import itertools

def pair_slide(l):
    return itertools.izip(l, l[1:])
```

```python
>>> list(pair_slide("ABCDEF"))
[('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')]
```

## Other

### Generate and execute dynamic Bash commands in Python

This can be very usefull to dynamically create Bash functions in Python. A good example is to dynamically set environment variables after getting them in Python.

Your Bash file need this:

```bash
eval "$(python print_bash_stuff.py)"
```

`print_bash_stuff.py` file just need to dynamically print bash commands:

```python
print 'function test {\n    echo "toto"\n}\n'
```
