LEDStrip
========

Python simulation of WS2812 (or probably other WS-type LEDs) LED strips commonly used by NeoPixel API.


## Example 
```
from led import LEDSim
import cv2
import numpy as np

pixel = LEDSim()
pixel.fill((0,0,0))

p = 0
for r in range(1,6):
	for g in range(1,6):
		for b in range(1,6):
			pixel[p] = (r,g,b)
			p += 1

pixel.visualize()
```