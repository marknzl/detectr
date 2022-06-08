import os

from flask import Flask, render_template, request
from os import path
from hashlib import md5
from webapp_utils import (
    get_license_plate,
    read_license_plate_text,
    filter_text
)

from flask import Flask, render_template

app = Flask(__name__)

@app.before_request
def create_static_folder_if_nonexistent():
    if not path.exists('static'):
        os.makedirs('static')

@app.route('/', methods=['GET', 'POST'])
def index():
    submitted = False
    hashed_filename = None
    extracted_filename = None
    raw_plate_text = None
    filtered_plate_text = None
    accuracy = None
    error_msg = None

    if request.method == 'POST':
        file = request.files['file']
        if file.filename.split('.')[1] != 'png':
            error_msg = 'Only PNGs allowed!'
        else:
            """
            I compute the MD5 hash of the image here to use as the
            unique file name. Also, I can use this to check if the same image
            is uploaded multiple times which allows me to mitigate
            expensive image processing operations.
            """

            md5_hash = md5(file.read()).hexdigest()
            hashed_filename = f'{md5_hash}.{file.filename.split(".")[1]}'
            file.seek(0)    # need to reset cursor position as we call file.read()

            try:
                # If same image is already uploaded, we don't process it again.
                if path.exists(f'static/{hashed_filename}'):
                    extracted_filename = f'{hashed_filename.split(".")[0]}_plate.{hashed_filename.split(".")[1]}'
                else:
                    file.save(f'static/{hashed_filename}')
                    extracted_filename = get_license_plate(hashed_filename)
                raw_plate_text, accuracy = read_license_plate_text(extracted_filename)
                filtered_plate_text = filter_text(raw_plate_text)
                submitted = True
            except:
                error_msg = 'An error occurred'
    
    return render_template('index.html',
                           submitted=submitted,
                           unmodified_filename=hashed_filename,
                           extracted_filename=extracted_filename,
                           raw_plate_text=raw_plate_text,
                           filtered_plate_text=filtered_plate_text,
                           accuracy=accuracy,
                           error_msg=error_msg)