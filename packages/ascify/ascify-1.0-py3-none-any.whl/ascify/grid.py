import os
import sys
import math
import numpy as np
from PIL import Image

from .renditions import default_rendition, default_tokens

class ResizeOptions:
    NEAREST  = Image.NEAREST  # 0x00
    LANCZOS  = Image.LANCZOS  # 0x01
    BILINEAR = Image.BILINEAR # 0x02
    BICUBIC  = Image.BICUBIC  # 0x03
    BOX      = Image.BOX      # 0x04
    HAMMING  = Image.HAMMING  # 0x05

class AsciiGrid:
    def __init__(self, impath, step=3, size=(60, 130), rendition=default_rendition,
                 ascii_tokens=default_tokens, resample=ResizeOptions.BILINEAR):
        if len(size) != 2:
            raise ValueError("provided size got invalid format, expected length "
                             f"= 2, but received: {len(size)}")
        if not os.path.exists(impath):
            raise FileNotFoundError(f"File by provided path '{impath}' "
                                     "wasn't found")

        self.rendition  = rendition
        self.tokens     = ascii_tokens

        self.y, self.x  = size
        size            = list(map(lambda x: x*step, size))
        self.step       = step
        self.img        = Image.open(impath).resize(size[::-1], resample=resample)
        self.img        = np.array(self.img)
        self.ascii_grid = ""

    def start(self):
        for i in range(self.y):
            self.ascii_grid += self._lstep(i)
        self.ascii_grid = self.ascii_grid[:-1]

    def _lstep(self, i):
        rv = ""
        for j in range(self.x):
            img_slice = self.img[i*self.step:(i+1)*self.step,
                                 j*self.step:(j+1)*self.step]
            rv += self.rendition(img_slice, self.tokens)
        return (rv+"\n")

    def __str__(self):
        return self.ascii_grid

    def __len__(self):
        return len(self.ascii_grid)
