from flask import request, send_file
from rembg import remove
import os

UPLOAD_FOLDER = 'uploads'

def remove_background(file):
    if file.filename == '':
        return "No selected file", 400
    
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    print(f"File saved: {file_path}")  # Debug statement

    # Remove the background
    try:
        with open(file_path, 'rb') as input_file:
            input_data = input_file.read()
            output_data = remove(input_data)
    except Exception as e:
        print(f"Error removing background: {e}")  # Debug statement
        return "Error removing background", 500

    # Get the selected output format
    output_format = request.form.get('bg-format', 'png')  # Default to PNG
    output_filename = f'no_background_{file.filename.rsplit(".", 1)[0]}.{output_format}'
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)

    with open(output_path, 'wb') as output_file:
        output_file.write(output_data)

    return send_file(output_path, as_attachment=True)
