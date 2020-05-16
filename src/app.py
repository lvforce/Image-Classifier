from flask import Flask, flash, request, redirect, render_template, url_for
import urllib.request
from werkzeug.utils import secure_filename
from train import train
from dataset import *
import os
from PIL import Image


app = Flask(__name__)
#UPLOAD_FOLDER = '/home/roman/projects/Image-Classifier/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg', 'webp'])
app.secret_key = "secret key"
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
net = train()

imsize = 256
loader = transforms.Compose([transforms.Resize((32, 32)),
                                transforms.ToTensor(),
                                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


@app.route('/predicted/<predicted_class>/<accuracy>')
def result(predicted_class, accuracy):
	return render_template('result.html', predicted_class=predicted_class, accuracy=accuracy)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
	return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
	class_correct = list(0. for i in range(10))
	class_total = list(0. for i in range(10))
	if request.method == 'POST':
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return request.redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print(file.filename)
			#file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			image = Image.open(file)
			image = loader(image).float()
			image = torch.autograd.Variable(image, requires_grad=True)
			image = image.unsqueeze(0)
			net.eval()
			output = net(image)
			conf, predicted = torch.max(output.data, 1) 
			print(classes[predicted.item()], "confidence: ", conf.item())
			return redirect(url_for('result', predicted_class = classes[predicted.item()], accuracy = float("{0:.1f}".format(conf.item()))))



if __name__ == "__main__":
	app.run(debug = True, port=os.getenv('PORT', 5000))