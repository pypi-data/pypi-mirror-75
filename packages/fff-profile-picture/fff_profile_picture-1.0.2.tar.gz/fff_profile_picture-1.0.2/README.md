# FFF Profile Picture Lib
## What is it?
A library to generate profile pictures

## Example
```python
from fff_profile_picture import Generator
from PIL import Image

generator = Generator(Image.open("original.JPG"), Image.open("overlay.png"))
result = generator.process()
result.save("generated.png")
```

## Docs

####`class Generator(self, background, overlay, scale=0, size=(640, 640))`

`background`: PIL.Image: An Image object representing 
the picture on that the overlay will be printed.

`overlay`: Pil.Image: An Image object representing the picture that 
will be used as an overlay

`scale`: Int: How thick the border should be. Defaults to 0

`size`: Tuple: Defines the size of the result. Background will be scaled to this 
size.

`process()`:

Creates the Picture

Returns: PIL.Image

