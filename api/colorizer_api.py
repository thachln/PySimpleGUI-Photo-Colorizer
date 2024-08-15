import cv2
import os

import numpy as np

import requests

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
            return self.response(200, message="Welcome to Colorizer API. To send an black and white image, please make a POST request using the same URL.")
        elif request.method == "POST":
            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            image_url = os.path.join(UPLOAD_FOLDER, file.filename)

            file.save(image_url)

            image, colorized = c.colorize_image(image_url)

            buffer = cv2.imencode('.jpg', colorized)[1].tobytes()

            io_buffer = io.BytesIO(buffer).getvalue()

            return send_file(io.BytesIO(io_buffer), mimetype='image/jpeg', as_attachment=True, download_name=file.filename)
