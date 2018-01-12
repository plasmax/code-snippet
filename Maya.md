# Maya Code Snippet

## Retrieve position of every vertices of mesh node

Very fast way to retrieve position of every vertices of mesh node.

```python
import maya.cmds as mc

raw_pos = mc.xform('pCube1.vtx[*]', query = True, worldSpace = True, translation = True)
vtx_pos = zip(raw_pos[0::3], raw_pos[1::3], raw_pos[2::3])
```

## Retrive index of the closest vertex of the given position

```python
import maya.cmds as mc

def sqrt_dst(p1,p2):
    """return square distance between `p1` and `p2`
    
    This assume `p1` and `p2` are tuple of three component each.
    """
    return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2

def closest(org_pos, node):
    """Return vertex indice of given node wich is the closest of given world space `org_pos`"""
    # get every world space position of given node vertices
    raw_pos = mc.xform(node+'.vtx[*]', query = True, worldSpace = True, translation = True)
    
    # convert raw list to list of three-component-tuple
    pt_pos = zip(raw_pos[0::3], raw_pos[1::3], raw_pos[2::3])
    
    pt_sqrt_dst = [sqrt_dst(org_pos, pt) for pt in pt_pos]
    
    return pt_sqrt_dst.index(min(pt_sqrt_dst))

# get world position of the locator
loc_pos = mc.xform('locator1', query = True, worldSpace = True, translation = True)

print closest(org_pos = loc_pos, node = 'pCube1')
```

## Iterate over top nodes of the current scene

```python
import maya.cmds as mc

# to avoid to get default cameras, we create a set with default nodes
defaultNodes = set(mc.ls(defaultNodes=True))

def top_nodes():

    # iter over every top transform nodes
    for node in mc.ls(assemblies = True):
        
        # skip default nodes and nodes having parent
        if node in defaultNodes:
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

## Convert non-ascii node names to valid ascii

Following previous snippet, this one will rename every node to ensure it has a ascii complient name.

```python
import unicodedata

import maya.cmds as mc

has_ascii = True

while has_ascii:
    
    for node in mc.ls('*'):
        try:
            node.decode('ascii')
        except UnicodeEncodeError:
            new_name = unicodedata.normalize('NFKD', node).encode('ascii', 'ignore')
            print "Rename non-ASCII node: ", node, "->", new_name
            mc.rename(node, new_name)
            break
    else:  # no break
        has_ascii = False
            
# Rename non-ASCII node:  pâté -> pate
```

You have to be careful as new name can potentially clash with another node.

This snippet is inspired from [here](http://sametmax.com/lencoding-en-python-une-bonne-fois-pour-toute/).

## Add a new menu

![Maya add_menu](img/maya/maya_add_menu.png)

```python
import maya.mel as mel

# get main window menu
mainMayaWindow = mel.eval('$nothing = $gMainWindow')

# top menu
menu = mc.menu('Coucou!', parent = mainMayaWindow)

mc.menuItem(label = "Another Manager", command = "print 'another manager'", parent = menu)

# optionnal: add another entry in the menu with a function instead of a string
def do_something(arg):
    print "Do something"

mc.menuItem(label = "Another Menu", command = do_something, parent = menu)
```

## Retrive currently selected camera

It looks like there is two way to retrive currently focused camera.

```python
import maya.cmds as mc

# method 1: get focused panel
focus_pan = mc.getPanel(withFocus=True)

# method 2: get what the playblast command consider as the active editor
focus_pan = mc.playblast(activeEditor=True)

# and finally get camera name from editor
cam = mc.modelPanel(focus_pan, query=True, camera=True)
```

If the focused panel is not a `modelEditor`, method 1 will bring to a `RuntimeError` when trying to retrieve camera name using `modelPanel`. Method 2 seems to be more reliable.


## Get materials connected to a list of shapes

You maybe know `hyperShade()` command to select materials connected to selected objects:

```python
>>> import maya.cmds as mc
>>> mc.hyperShade(mc.hyperShade(shaderNetworksSelectMaterialNodes=True)
>>> mc.ls(selection=True)
[u'lambert1']
```
But this command need UI.

Here is a version relying on connections:

```python
>>> mshs = ['pSphereShape1']
>>> sgs = mc.listConnections(mshs, type='shadingEngine')
>>> sg_inputs = mc.listConnections(sgs, destination=False)
>>> mc.ls(sg_inputs, materials=True)
[u'lambert1']
```

## Maya Python Idioms

Those are idioms to do various things in Maya.

### Get node name

If you want to get node name from a given node path, you can use `split('|')[-1]` and be sure to get the node name.

```python
>>> '|path|to|node'.split('|')[-1]  # full node path
'node'
>>> 'path|to|node'.split('|')[-1]  # relative node path
'node'
>>> 'node'.split('|')[-1]  # even node name works
'node'
```

### Get parent name from absolute node path

A safe way to get parent is to do:

```python
>>> mc.listRelatives('|path|to|node', parent=True, fullPath=True)[0]
'|path|to'
```

The `listRelatives()` command return a `list` of parent node paths. A node can have multiple parent in case of instance (one shape, multiple parent `transform` nodes).

But `listRelatives()` is costly. If you have the garanty there is no instance in your scene and the input node path is absolute you can rely on string manipulation and use `rsplit('|', 1)` to cut the string on the right and get parent node:

```python
>>> '|path|to|node'.rsplit('|', 1)[0]
'|path|to'
```

### Get absolute node path from relative node path

Some commands can't return absolute node path. The way to get absolute node path from relative node path is:

```python
>>> mc.ls('to|node', long=True)[0]
'|path|to|node'
```
