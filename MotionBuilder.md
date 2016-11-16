# MotionBuilder Code Snippet

## Get selection

```python
import pyfbsdk as mb

# create empty model list
models = mb.FBModelList()

# fill list with every selected model in scene
mb.FBGetSelectedModels(models)
```

## Get current file path

```python
import pyfbsdk as mb

mb.FBApplication().FBXFileName
```

## Walk recursively through hierarchy

```python
def walk(model):
    for child in model.Children:
        yield child
        for sub_child in walk(child):
            yield sub_child
```

# Walk through parents

```python
def walk_top(model):
    parent = model.Parent

    if not parent:
        raise StopIteration

    yield parent

    for grand_parent in walk_top(parent):
        yield grand_parent
```

## Clear selection

```python
import pyfbsdk as mb

def clear_selection():

    # get selection
    models = mb.FBModelList()
    mb.FBGetSelectedModels(models)

    # remove models from selection
    for models in models:
        models.Selected = False
```
