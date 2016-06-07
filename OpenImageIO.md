# OpenImageIO

## Handle Errors

```python
import OpenImageIO as oiio

img_path = "/path/to/your/image.exr"

# read image
buf = oiio.ImageBuf(img_path)

if buf.has_error:
    print "Reading image: {0}".format(buf.geterror())
    exit()

# get spec
spec = src_buf.spec()

if buf.has_error:
    print "Getting image specs: {0}".format(buf.geterror())
    exit()

# apply algo
res = oiio.ImageBufAlgo.zero(out_buf)

# algo errors are handled using a return value
if not res:
    print "Zeroing output buffer: {0}".format(oiio.geterror())
    exit()

# write
out_buf = oiio.ImageBuf(spec)
out_buf.write(dst_path)

if out_buf.has_error :
    print "Writting buffer: {0}".format(out_buf.geterror())
    exit()

# etc...
```

## List metadatas

```python
import OpenImageIO as oiio

img_path = "/path/to/your/image.exr"

# read image
buf = oiio.ImageBuf(img_path)

# get spec
spec = buf.spec()

# get attributes of the buffer
attrs = spec.extra_attribs

# and list them (the old way)
for i in xrange(len(attrs)):
    attr = attrs[i]
    print attr.name, attr.type, attr.value

# more pythonic way
for attr in attrs:
    print attr.name, attr.type, attr.value
```

## Resize image

```python
import OpenImageIO as oiio

img_path = "/path/to/your/image.exr"

# read image
buf = oiio.ImageBuf(img_path)

spec = buf.spec()
spec.full_width  = 32
spec.full_height = 32

out_buf = oiio.ImageBuf(spec)

# filter names can be:
# lanczos3, box, triangle, catrom, blackman-harris, gaussian, mitchell,
# bspline, radial-lanczos3, disk, sinc
oiio.ImageBufAlgo.resize(out_buf, buf, filtername="lanczos3")

# write
out_buf.write(dst_path)
```
