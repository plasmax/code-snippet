# Maya Code Snippet

## Iterate over top nodes of the current scene

```python
import maya.cmds as mc

# to avoid to get default cameras, we create a set with default nodes
defaultNodes = set(mc.ls(defaultNodes=True))

def top_nodes():

    # iter over every transform node of the scene
    for node in mc.ls(type="transform"):
        
        # skip default nodes and nodes having parent
        if any((node in defaultNodes,
                mc.listRelatives(node, parent=True))):
            continue

        yield node
```

From an empty scene, create a group (ctrl+g):

![Maya empty group](img/maya/maya_null_grp.png)

```python
print list(top_nodes())
# [u'null1']
```

## Iterate over nodes having non-ascii characters in their names

This snippet run though every node in the current scene and detect if there is non ascii characters in node names.

```python
import maya.cmds as mc

def non_ascii_named_nodes():

	# iterate over every node of the current scene
	for node in mc.ls('*'):

		# try to read node name in ascii...
		try:
			node.decode('ascii')
		except UnicodeEncodeError:
			# ...and return the node if its fail
			yield node
```

Create a null node and rename it "pâté" then run the command:

```python
print list(non_ascii_named_nodes())
# [u'p\xe2t\xe9']
```

Maya can print correct values like this:

```python
for node in non_ascii_named_nodes():
    print node
# pâté
```
