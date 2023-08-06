# simplemosaic


## Getting Started




### Installing



```bash
pass
```

### Usage



```python
from ... import Converter, Mosaic, load_images
import cv2 as cv
image = Converter.load('default.jpeg')
images = load_images('pics')
mosaic = Mosaic(image, images, (70, 70), ratio=3000).create()
cv.imwrite("mosaic.jpg", mosaic)
```





## Authors

* **Jakub Szkodny** - [szjakub](https://github.com/szjakub)

