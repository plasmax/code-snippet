# OpenImageIO

## Handle Errors

OpenImageIO doesn't handle errors the most pythonic way. This mean you often have to catch them by yourself.

```python
import OpenImageIO as oiio

img_path = "/path/to/your/image.exr"

# read image
buf = oiio.ImageBuf(img_path)

if buf.has_error:
    raise Exception("Reading image: {0}".format(buf.geterror())

# get spec
spec = src_buf.spec()

if buf.has_error:
    raise Exception("Getting image specs: {0}".format(buf.geterror()))

# apply algo
res = oiio.ImageBufAlgo.zero(out_buf)

# algo errors are handled using a return value
if not res:
    raise Exception("Zeroing output buffer: {0}".format(oiio.geterror()))

# write
out_buf = oiio.ImageBuf(spec)
out_buf.write(dst_path)

if out_buf.has_error :
    raise Exception("Writting buffer: {0}".format(out_buf.geterror()))

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

# copy and modify the spec
spec = buf.spec()
spec.full_width  = 32
spec.full_height = 32

# generate a new buffer using the modified spec
out_buf = oiio.ImageBuf(spec)

# filter names can be:
# lanczos3, box, triangle, catrom, blackman-harris, gaussian, mitchell,
# bspline, radial-lanczos3, disk, sinc
oiio.ImageBufAlgo.resize(out_buf, buf, filtername="lanczos3")

# write
out_buf.write(dst_path)
```
