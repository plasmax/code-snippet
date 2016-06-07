# Mari Code Snippets

## Mari's Python API documentation

Mari's Python API documentation is in _Help/SDK/Python/Documentation_.

The top of each class documentation contain:

* Current class hierarchy
* A short description of the class purpose
* And sometime a code example

Class hierarchy is useful to know which other functions can be used, don't forget them!

## Mari's Python Examples

There is also some example scripts in _Help/SDK/Python/Open Examples Folder_.

Once you get familiar with basic Mari Python concept you should be comfortable with them.

## Geometry

Listed in Mari UI in the _Objects_ Palette.

`mari.geo` is a `GeoManager` object. It's often the starting point to get infos from Mari objects.

```python
import mari

# get object names
print mari.geo.names()

# get a GeoEntity object from its name
print mari.geo.get('my_geo')

# remove an object from its name
mari.geo.remove('my_geo')

# iterate over every objects in the scene
for geo in mari.geo.list():
    print geo.name()

# get the currently selected GeoEntity object
print mari.geo.current()

# hide and show object
geo.hide()
print geo.isVisible() # return False

geo.show()
print geo.isVisible() # return False

# another way to show/hide object
geo.setVisibility(True)

# lock and unlock object
geo.lock()
print geo.isLocked() # return True

geo.unlock()
print geo.isLocked() # return False

# another way to lock/unlock object
geo.setLocked(True)
```

### Generate subdivision surface 

```python
import mari

# get the currently selected geo
geo = mari.geo.current()

# apply subdivision (note that "Level" to 3 mean three subdivision levels: 0, 1 and 2)
geo.generateSubdivision({"Level":3,
                         "Scheme":"Catmull Clark",
                         "Force":True,
                         "Boundary Interpolation":"Edge And Corner"});

# change subdivision level
geo.setSubdivisionLevel(1)

print geo.maximumSubdivisionLevel() # should return 2
```

## Metadata

Python objects of type `mari.Metadata`. Most Mari Python objects support metadata: `Layer`, `Camera`, `GeoEntity`, etc... See _Subclasses_ in class hierarchy to get them all.

```python
import mari

# get the currently selected geo
geo = mari.geo.current()

# iterate over metadatas
for name in geo.metadataNames():
  print "Name:", name
  print "Value:", geo.metadata(name)
  print "Default Value:", geo.metadataDefault(name)
  print "Description:", geo.metadataDescription(name)
  print "Display Name:", geo.metadataDisplayName(name)
```
