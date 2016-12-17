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

## Walk through top models of the current scene

Source [here](http://awforsythe.com/tutorials/pyfbsdk-4).

```python
import pyfbsdk as mb

def top_models():
    """Iterate over models on top of the hierarchy

    :return: iterator of models of the top of the hierarchy
    :rtype: `generator` of `pyfbsdk.FBModel`
    """
    for model in mb.FBSystem().Scene.RootModel.Children:
        yield model
``

## Walk recursively through hierarchy

```python
def walk(model):
    for child in model.Children:
        yield child
        for sub_child in walk(child):
            yield sub_child
```

## Walk through parents

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

## Switch/Get time in frame or timecode

MotionBuilder return time string depending on the display time mode so this mode need to be switched before getting time string.

```python
import pyfbsdk as mb

# get player control
player = mb.FBPlayerControl()

# TransportTimeFormat is a read write property
# here we set in timecode
player.TransportTimeFormat = mb.FBTransportTimeFormat.kFBTimeFormatTimecode

# get the FBTime object of the start frame
mb_time = mb.FBSystem().CurrentTake.LocalTimeSpan.GetStart()

# will return formatted time code: 00:00:04:05
print mb_time.GetTimeString()

# now we change to frame
player.TransportTimeFormat = mb.FBTransportTimeFormat.kFBTimeFormatFrame

# get the FBTime object again
mb_time = mb.FBSystem().CurrentTake.LocalTimeSpan.GetStart()

# will return formatted frame: 101
print mb_time.GetTimeString()
```
