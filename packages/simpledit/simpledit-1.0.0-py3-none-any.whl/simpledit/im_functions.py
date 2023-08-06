from PyQt5 import QtGui
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from skimage.transform import swirl
import math
import numpy
import copy
import numpy
import os

### Color ###

def adjust_brightness(img, val):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(val)

def adjust_contrast(img, val):
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(val)

def adjust_saturation(img, val):
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(val)

def adjust_transparency(img, perc):
    arr = numpy.array(img)
    arr_A = arr[:, :, 3]

    if perc < 1:
        val = int((1 - perc) * 255)
        arr_A[arr_A < val] = 0
        arr_A[arr_A >= val] -= val
    elif perc > 1:
        val = int((perc - 1) * 255)
        arr_A[(arr_A > 0) & (arr_A > 255 - val)] = 255
        arr_A[(arr_A > 0) & (arr_A <= 255 - val)] += val

    arr[:, :, 3] = arr_A
    return Image.fromarray(arr)

def blend(img1, img2, amt):
    h, w=img1.size
    img2=img2.resize((h,w))
    a= Image.blend(img1, img2,amt)
    return a

### Effects ###

def swirl_effect(img):
    arr = numpy.array(img)
    width, height = img.size 
    im = swirl(arr, rotation=0, strength=4, radius=height)
    im = (im * 255).astype(numpy.uint8)
    return Image.fromarray(im)

def blur(img):
    return img.filter(ImageFilter.GaussianBlur(radius = 5)) 

def edge_enhance(img): 
    return img.filter(ImageFilter.EDGE_ENHANCE) 

def smooth(img): 
    return img.filter(ImageFilter.SMOOTH_MORE)

def pixelate(img): 
    width, height = img.size
    img_small = img.resize((int(width/15),int(height/10)))
    return img_small.resize(img.size, Image.NEAREST)

def create_border(img, borderSize, borderColor):
    return ImageOps.expand(img, round(borderSize), borderColor)

### Edit ###

def left_rotate(img):
    return img.transpose(Image.ROTATE_90)

def right_rotate(img):
    return img.transpose(Image.ROTATE_270)

def flip(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)

def crop(img, w1, h1, w2, h2):
    if w1!=w2 and h1 != h2:
        return img.crop((w1, h1, w2, h2))

### Filters ###

def invert_filter(img): 
    arr = numpy.array(img) 
    arr[:,:,0:3] = 255 - arr[:,:,0:3]
    return Image.fromarray(arr)

def grayscale_filter(img):
    arr = numpy.array(img)
    gr = arr[:,:,0] * 0.07 + arr[:,:,1] * 0.72 + arr[:,:,2] * 0.21
    gr[gr > 255] = 255
    arr[:,:,0] = gr
    arr[:,:,1] = gr
    arr[:,:,2] = gr
    return Image.fromarray(arr)

def sepia_filter(img):
    arr = numpy.array(img)

    sepia_r =  arr[:,:,0] * 0.393 + arr[:,:,1] * 0.769 + arr[:,:,2] * 0.189
    sepia_g =  arr[:,:,0] * 0.349 + arr[:,:,1] * 0.686 + arr[:,:,2] * 0.168
    sepia_b =  arr[:,:,0] * 0.272 + arr[:,:,1] * 0.534 + arr[:,:,2] * 0.131

    sepia_r[sepia_r > 255] = 255
    sepia_g[sepia_g > 255] = 255
    sepia_b[sepia_b > 255] = 255

    arr[:,:,0] = sepia_r
    arr[:,:,1] = sepia_g
    arr[:,:,2] = sepia_b

    return Image.fromarray(arr)

def color_filter(img, r_val, g_val, b_val):
    arr = numpy.array(img)

    arr_R = arr[:, :, 0] > 255 - r_val
    arr_G = arr[:, :, 1] > 255 - g_val
    arr_B = arr[:, :, 2] > 255 - b_val

    arr[arr_R, 0] = 255 - r_val
    arr[arr_G, 1] = 255 - g_val
    arr[arr_B, 2] = 255 - b_val

    arr[:, :, 0] += r_val
    arr[:, :, 1] += g_val
    arr[:, :, 2] += b_val

    return Image.fromarray(arr)

def invert_filter(img):
    arr = numpy.array(img)
    arr[:, :, 0:3] = 255 - arr[:, :, 0:3]
    return Image.fromarray(arr)