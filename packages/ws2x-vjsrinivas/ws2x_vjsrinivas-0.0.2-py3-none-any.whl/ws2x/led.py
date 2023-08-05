import cv2
import numpy as np
import logging

class LEDSim:
    def __init__(self, length=144):
        self.length = length
        
        self._WARN_NATIVE_MSG = "LED strip function called is not native to NeoPixel API"
        self._WARN_GENERAL_MSG = "Code invoked is from LED simulator"
        self.WS28X_LED = [(0,0,0) for i in range(length)]
        
        logging.basicConfig(level=logging.WARNING)
        logging.warn(self._WARN_GENERAL_MSG)

    def __setitem__(self, index, value):
        self.WS28X_LED[index] = value

    def __getitem__(self, index):
        return self.WS28X_LED[index]

    def get_led(self):
        return self.WS28X_LED

    def visualize(self,size=(100,1800,3), waittime=-1):
        logging.warn(self._WARN_NATIVE_MSG)
        img = np.full(size, 255).astype(np.uint8)
        # generate led strip:
        # rectangle size = (x,y) and (x+rsize, y+rsize)
        padding = 2
        rsize = 10
        needed_length = 2+((10*self.length)+(2*self.length))+2;
        start_pos = (30,50-rsize)

        # generate white backing:
        cv2.rectangle(img, start_pos, (start_pos[0]+needed_length-padding, start_pos[1]+rsize+(padding*2)), (0,0,0), 1)
        
        for i,led in enumerate(self.WS28X_LED):
            #led -> (rgb)
            # flip for cvv2
            #color = (led[2], led[1], led[0])
            color = led
            cv2.rectangle(img, \
                (start_pos[0]+(padding+((rsize+padding)*i)), start_pos[1]+padding), \
                (start_pos[0]+(padding+((rsize+padding)*i)+rsize), start_pos[1]+padding+rsize), \
                color, \
                -1)

        cv2.imshow('visualize',img)
        
        if waittime != 0:
            cv2.waitKey(waittime)
        
    def reset(self):
        logging.warn(self._WARN_NATIVE_MSG)
        self.WS28X_LED = [(0,0,0) for i in range(self.length)]

    def fill(self, color):
        assert type(color) == tuple and len(color) == 3
        self.WS28X_LED = [color for i in range(self.length)]

    def get_length(self):
        logging.warn(self._WARN_NATIVE_MSG)
        return self.length

# debugging:

if __name__ == '__main__':
    led = LEDSim()
    led[0] = (255,0,255)
    led.visualize()

