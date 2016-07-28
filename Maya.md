# Maya Code Snippet

## Iterate over top nodes of the current scene

```python
import maya.cmds as mc

# to avoid to get default cameras, we create a set with default nodes
defaultNodes = set(mc.ls(defaultNodes=True))

def top_nodes() :

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
