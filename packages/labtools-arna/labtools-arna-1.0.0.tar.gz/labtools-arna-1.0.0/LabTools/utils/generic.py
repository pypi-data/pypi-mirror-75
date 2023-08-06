
#  LabTools - generic.py
#  Copyright 2019 Luca Arnaboldi

import inspect
from PIL import Image
from uncertainties import unumpy as unp
import numpy as np

def sprint(obj):
    """
    Super Print. Print a variable with its name.
    """
    def retrieve_name(var):
        """
        Copy-pasted from StackOverflow
        """
        callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
        return [var_name for var_name, var_val in callers_local_vars if var_val is var]

    obj_name = retrieve_name(obj)[0]

    print("{0}: {1}".format(obj_name, obj))

def decibel(x):
    """
    Convert a value in decibel.
    """
    return 20. * unp.log10(x)

def deg2rad(deg, prim = None, sec = None):
    """
    Convert a value from degree to radiants
    """
    if sec is not None:
        rad_sec = sec / 3600. * np.pi / 180.
    else:
        rad_sec = 0.
    if prim is not None:
        rad_min = prim / 60. * np.pi / 180.
    else:
        rad_min = 0.
    rad_deg = deg * np.pi / 180.
    return rad_deg+rad_min+rad_sec

def rad2deg(rad):
    """
    Convert radiants to degrees (not supported the notation with minute and seconds)
    """
    return rad/np.pi * 180.


def crop_oscilloscope_image(image, result_image = None, area = None):
    """
    Crop an acquisition of oscilloscope screen and save it in result_image.
    If result_image is None, the image is overwritten.
    Border define the interesting area. If None the default is used.
    """
    AREA = (0, 23, 317, 245)

    if result_image is None:
        result_image = image
    if area is None:
        area = AREA

    img = Image.open(image)
    cropped_img = img.crop(AREA)

    cropped_img.save(result_image)
