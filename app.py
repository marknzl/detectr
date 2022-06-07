from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    submitted = False
    hashed_filename = None
    extracted_filename = None
    raw_plate_text = None
    filtered_plate_text = None
    accuracy = None
    error_msg = None
    
    return render_template('index.html',
                           submitted=submitted,
                           unmodified_filename=hashed_filename,
                           extracted_filename=extracted_filename,
                           raw_plate_text=raw_plate_text,
                           filtered_plate_text=filtered_plate_text,
                           accuracy=accuracy,
                           error_msg=error_msg)