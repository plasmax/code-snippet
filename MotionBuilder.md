# MotionBuilder Code Snippet

## Get selection

```python
import pyfbsdk as mb

# create empty model list
models = mb.FBModelList()

# fill list with every selected model in scene
mb.FBGetSelectedModels(models)

# print the name of the first selected model
print models[0].LongName
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

## Get list of property on a particular model

```python

import pyfbsdk as mb

# create empty model list
models = mb.FBModelList()

# fill list with every selected model in scene
mb.FBGetSelectedModels(models)

# iterate over property of the model
for prop in models[0].PropertyList:
        
    print type(prop), prop.Name

    # python can't access datas for some types (FBPropertyAction, FBPropertyListObject, etc.)
    # that's why we use try/except
    try:
        print "VALUE", type(prop.Data), prop.Data
    except NotImplementedError:
        continue
```

## Get Story tracks and clips

```python
import pyfbsdk as mb

# retrieve the root of the story object
story = mb.FBStory()
root_story = story.RootFolder

# we need this to find character 
scene = mb.FBSystem().Scene

# browse animation tracks
for track in root_story.Tracks:

    print type(track), track.LongName
    print "Mute", track.Mute
    print "Type", track.Type  # can't be mb.FBStoryTrackType.kFBStoryTrackCharacter for example

    # iterate over clips
    for clip in track.Clips:
    
        print type(clip), clip.LongName
        
        frame_start = clip.Start.GetFrame(mb.FBTimeMode.kFBTimeMode24Frames)
        frame_stop = clip.Stop.GetFrame(mb.FBTimeMode.kFBTimeMode24Frames)
        
        mark_in = clip.MarkIn.GetMilliSeconds()
        mark_out = clip.MarkOut.GetMilliSeconds()
        
        print frame_start, frame_stop, mark_in, mark_out
```
