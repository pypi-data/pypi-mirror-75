
from LabTools.utils.generic import *
from uncertainties import ufloat, unumpy
import cv2
import filecmp

def float_equal(x, y, accuracy):
    return (1. - accuracy) <= x / y and x / y  <= (1. + accuracy)

def image_equal(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())


def test_sprint(capfd):
    a = 'marco'
    b = 45.
    c = [12, 45]
    d = ufloat(b,b)
    e = unumpy.uarray(c, c)

    sprint(a)
    out, err = capfd.readouterr()
    assert(out == 'a: marco\n')

    sprint(b)
    out, err = capfd.readouterr()
    assert(out == 'b: 45.0\n')

    sprint(c)
    out, err = capfd.readouterr()
    assert(out == 'c: [12, 45]\n')

    sprint(d)
    out, err = capfd.readouterr()
    assert(out == 'd: (4+/-4)e+01\n')

    sprint(e)
    out, err = capfd.readouterr()
    assert(out == 'e: [12.0+/-12.0 45.0+/-45.0]\n')

def test_decibel():
    assert(float_equal(decibel(0.5), -6.0205999132796239042747778944898, 1e-6))
    assert(float_equal(decibel(10.), 20., 1e-6))

    # With uncertainties
    a = ufloat(10., 1.)
    assert(str(decibel(a)) == "20.0+/-0.9")

def test_crop_oscilloscope_image():
    crop_oscilloscope_image('test/inputs/to_crop.png', 'test.tmp.png')

    correct = cv2.imread('test/outputs/cropped.png')
    produced = cv2.imread('test.tmp.png')
    print(correct - produced)

    assert(image_equal(correct, produced))

def test_conversion_deg_rad():
    assert(deg2rad(1.) == 0.017453292519943295)
    assert(deg2rad(0., 60.) == 0.017453292519943295)
    assert(deg2rad(0., 0., 3600.) == 0.017453292519943295)

    assert(rad2deg(0.017453292519943295) == 1.)
