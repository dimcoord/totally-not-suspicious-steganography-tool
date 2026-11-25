import os
import processor
from flask import Flask, request, render_template

app = Flask(__name__)    

app.config['UPLOAD_FOLDER'] = 'input/'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

def allowed_file(filename):
    return '.' in filename and os.path.splitext(filename)[1].lower() in app.config['UPLOAD_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		file = request.files['file']
		message = request.form.get('message')
		if file and allowed_file(file.filename):
			filename = file.filename
			path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(path)
			# processor.process(path)
			processor.build_cipher(message)
			return render_template("index.html")
			# plaintext, ciphertext = processor.process(path)
			# return render_template("index.html", ptxt=plaintext, ctxt=ciphertext)
		else:
			return 'gak boleh', 400
	return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
