import cv2
import os

import io
from flask_appbuilder.api import BaseApi, expose
from flask import request, send_file
from werkzeug.utils import secure_filename

from imager.color import Colorizer

UPLOAD_FOLDER = 'api/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    """
    This function is used to check if a file is an allowed extension.
    :param filename: (str) full filename
    :return: (bool) True or False
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ColorizerApi(BaseApi):
    route_base = "/api"

    @expose('/colorizer', methods=["GET", "POST"])
    def colorize(self):
        prototxt = r'../model/colorization_deploy_v2.prototxt'
        model = r'../model/colorization_release_v2.caffemodel'
        points = r'../model/pts_in_hull.npy'

        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        c = Colorizer(prototxt, model, points)

        if request.method == "GET":
            return self.response(200, message="Welcome to Colorizer API. To send an black and white image, please make a POST request using the same URL.")
        elif request.method == "POST":
            if 'file' not in request.files:
                return self.response(404, message="No file part")

            file = request.files['file']

            if file.filename == '':
                return self.response(404, message="No selected file")

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image_url = os.path.join(UPLOAD_FOLDER, filename)
                file.save(image_url)
                image, colorized = c.colorize_image(image_url)
                buffer = cv2.imencode('.jpg', colorized)[1].tobytes()
                io_buffer = io.BytesIO(buffer).getvalue()
                return send_file(io.BytesIO(io_buffer), mimetype='image/jpeg', as_attachment=True, download_name=file.filename)
