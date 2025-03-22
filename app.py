from flask import Flask, request, render_template, send_file
from PIL import Image
import os

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
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Get the selected format
    selected_format = request.form['format']
    converted_path = os.path.join(UPLOAD_FOLDER, f'converted_image.{selected_format}')  # Use selected format

    img = Image.open(file_path)

    if selected_format == 'pdf':
        # Convert to PDF
        img.save(converted_path, "PDF", resolution=100.0)
    else:
        # Save with the selected format
        img.save(converted_path, format=selected_format.upper())

    return send_file(converted_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 