from flask import Flask, render_template, request, redirect, send_file
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resize', methods=['POST'])
def resize_image():
    if 'image' not in request.files:
        return 'No file uploaded', 400

    file = request.files['image']
    
    if file.filename == '':
        return 'No selected file', 400

    if file:
        # Save uploaded image
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        # Get new dimensions from the form
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))

        # Open the image and resize it
        img = Image.open(image_path)
        img_resized = img.resize((width, height))

        # Save the resized image
        resized_path = os.path.join(UPLOAD_FOLDER, 'resized_' + file.filename)
        img_resized.save(resized_path)

        return send_file(resized_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
