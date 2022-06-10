import os

from flask import Flask, render_template, request
from os import path
from hashlib import md5
from webapp_utils import (
    STATIC_PATH,
    get_license_plate,
    read_license_plate_text,
    filter_text
)

from flask import Flask, render_template

app = Flask(__name__)

@app.before_request
def create_static_folder_if_nonexistent():
    if not path.exists(str(STATIC_PATH)):
        os.makedirs(str(STATIC_PATH))

@app.route('/', methods=['GET', 'POST'])
def index():
    submitted = False
    hashed_filename = None
    license_plate_filename = None
    raw_plate_text = None
    filtered_plate_text = None
    accuracy = None
    error_msg = None

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.split('.')[1] != 'png':
                error_msg = 'Only PNGs allowed!'
            else:
                try:
                    """
                    I compute the MD5 hash of the image here to use as the
                    unique file name. Also, I can use this to check if the same image
                    is uploaded multiple times which allows me to mitigate
                    expensive image processing operations.
                    """

                    md5_hash = md5(file.read()).hexdigest()
                    hashed_filename = f'{md5_hash}.{file.filename.split(".")[1]}'
                    file.seek(0)    # need to reset cursor position as we call file.read()

                    # If same image is already uploaded, we don't process it again.
                    if path.exists(STATIC_PATH / hashed_filename):
                        license_plate_filename = f'{hashed_filename.split(".")[0]}_plate.{hashed_filename.split(".")[1]}'
                    else:
                        file.save(STATIC_PATH / hashed_filename)
                        license_plate_filename = get_license_plate(hashed_filename)
                    raw_plate_text, accuracy = read_license_plate_text(license_plate_filename)
                    filtered_plate_text = filter_text(raw_plate_text)
                    submitted = True
                except Exception as e:
                    os.remove(STATIC_PATH / hashed_filename)
                    error_msg = f'An error occurred: {e}'
    
    return render_template('index.html',
                           submitted=submitted,
                           unmodified_filename=hashed_filename,
                           license_plate_filename=license_plate_filename,
                           raw_plate_text=raw_plate_text,
                           filtered_plate_text=filtered_plate_text,
                           accuracy=accuracy,
                           error_msg=error_msg)