from flask import Flask, request, render_template, send_file
from PIL import Image
import os
import io
from remove_background import remove_background  # Import the new function
import threading
import time

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

    # Use a context manager to open the image
    with Image.open(file) as img:
        img.thumbnail((800, 800))  # Resize to a maximum of 800x800 while maintaining aspect ratio
        
        # Create an in-memory bytes buffer
        img_byte_arr = io.BytesIO()
        img.convert('RGB').save(img_byte_arr, format=output_format.upper())  # Save in the desired format
        img_byte_arr.seek(0)  # Move to the beginning of the BytesIO buffer

    return send_file(img_byte_arr, as_attachment=True, download_name=f"converted_image.{output_format}")

def delete_all_files(folder_path):
    # Wait for 1 minute before deleting
    time.sleep(60)
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting files: {e}")

@app.route('/remove-background', methods=['POST'])
def remove_bg():
    file = request.files['file']
    filename = file.filename
    if filename == '':
        return "No selected file", 400
    
    return remove_background(file, filename)  # Pass the file object and filename

def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        img = img.resize(size)
        img.save(output_path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use the PORT environment variable or default to 10000
    app.run(host='0.0.0.0', port=port, debug=False)  # Bind to 0.0.0.0 