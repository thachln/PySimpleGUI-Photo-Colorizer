import cv2
import os

import numpy as np

import io
from flask_appbuilder.api import BaseApi, expose
from flask import request, send_file, jsonify

from imager.color import Colorizer

UPLOAD_FOLDER = 'api/uploads'

class ColorizerApi(BaseApi):

    route_base = "/api"
    @expose('/colorizer', methods=["GET", "POST"])
    def colorize(self):
        prototxt = r'../model/colorization_deploy_v2.prototxt'
        model = r'../model/colorization_release_v2.caffemodel'
        points = r'../model/pts_in_hull.npy'

        file = request.files['file']

        c = Colorizer(prototxt, model, points)

        if request.method == "GET":
            return self.response(200, message="Welcome to Colorizer API.")
        elif request.method == "POST":
            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            image_url = os.path.join(UPLOAD_FOLDER, file.filename)

            file.save(image_url)

            image, colorized = c.colorize_image(image_url)
            image_bytes = colorized.tobytes()
            # mem = io.BytesIO()
            # mem.write(image_bytes)
            # mem.seek(0)
            print(image_bytes)
            return self.response(200, data="colorized")
