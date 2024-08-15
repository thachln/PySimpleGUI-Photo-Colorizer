import unittest
from imager.color import Colorizer
import cv2
import os

class TestColorizer(unittest.TestCase):
    def test_1(self):

        prototxt = r'../model/colorization_deploy_v2.prototxt'
        model = r'../model/colorization_release_v2.caffemodel'
        points = r'../model/pts_in_hull.npy'

        c = Colorizer(prototxt, model, points)

        image, colorized = c.colorize_image('data/1.png')
        self.assertIsNotNone(colorized)  # add assertion here

        if not os.path.exists('out'):
            os.mkdir('out')

        cv2.imwrite('out/1_c.png', colorized)


if __name__ == '__main__':
    # Create out folder to store colorized images.
    unittest.main()
