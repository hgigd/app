from flask import Flask, request, render_template, send_file
from PIL import Image
import os
from remove_background import remove_background  # Import the new function

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_image():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    # Get the selected output format
    output_format = request.form.get('format', 'png').lower()  # Ensure it's lowercase

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Convert the image to the desired format
    output_filename = f"{os.path.splitext(file.filename)[0]}.{output_format}"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)

    # Use a context manager to open the image
    with Image.open(file_path) as img:
        img.thumbnail((800, 800))  # Resize to a maximum of 800x800 while maintaining aspect ratio
        img.convert('RGB').save(output_path, format=output_format.upper())  # Save in the desired format

    return send_file(output_path, as_attachment=True)

@app.route('/remove-background', methods=['POST'])
def remove_bg():
    file = request.files['file']
    return remove_background(file)  # Call the function from the new file

def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        img = img.resize(size)
        img.save(output_path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)  # Bind to 0.0.0.0 