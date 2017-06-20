# Maya API Code Snippet

## Get active selection list

```python
import maya.OpenMaya as om

sel = om.MSelectionList()

om.MGlobal.getActiveSelectionList(sel)
```

## Iterate over Maya ui as PySide objects

```python
import maya.OpenMayaUI as omui
from PySide import QtCore, QtGui
import shiboken
 
mayaMainWindow = shiboken.wrapInstance(long(omui.MQtUtil.mainWindow()), QtGui.QWidget)
 
def print_children(widget, depth = 0):
    for child in widget.children():
        print '    '*depth, type(child), child.objectName()
        print_children(child, depth + 1)
 
print_children(mayaMainWindow)
```

More infos about MQtUtil [here](http://help.autodesk.com/view/MAYAUL/2017/ENU/?guid=__cpp_ref_class_m_qt_util_html)

## Convert MFloatMatrix to MMatrix

Using Maya API, you often have to convert a `MFloatMatrix` type to `MMatrix` type. The simpler way to do it in Python is this way:

```python
import maya.OpenMaya as om

my_float_mtx = om.MFloatMatrix()
my_mtx = om.MMatrix(my_float_mtx.matrix)
```

This rely on the `MFloatMatrix.matrix` property which is of type `float [4][4]` using the `MMatrix(const float m[4][4])` constructor.
