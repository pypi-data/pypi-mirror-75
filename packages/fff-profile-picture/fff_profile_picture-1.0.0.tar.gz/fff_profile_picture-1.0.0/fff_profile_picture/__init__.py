# !/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageOps


class Generator:
    def __init__(self, background, overlay, scale=0, size=(640, 640)):
        self.overlay = overlay
        self.background = background
        self.scale = scale
        self.size = size

    @classmethod
    def _add_border(cls, img, border):
        if isinstance(border, int) or isinstance(border, tuple):
            bimg = ImageOps.expand(img, border=border)
        else:
            raise RuntimeError('Border is not an integer or tuple!')
        return bimg

    def process(self):
        background = self.background.resize(self.size)
        background = background.convert('RGBA')
        background = self._add_border(background, self.scale)
        foreground = self.overlay.convert('RGBA').resize(background.size)

        result = Image.alpha_composite(background, foreground)
        return result
