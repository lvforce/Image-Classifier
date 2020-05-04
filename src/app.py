from flask import Flask, flash, request, redirect, render_template, url_for
import urllib.request
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = '/home/roman/projects/Image-Classifier/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg', 'webp'])
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
	return render_template('index.html')



app.run(debug = True)