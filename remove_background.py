from flask import request, send_file
from rembg import remove
import os
import io

UPLOAD_FOLDER = 'uploads'

def remove_background(file, filename):
    if filename == '':
        return "No selected file", 400

    # Read the file data
    input_data = file.read()

    # Remove the background
    try:
        output_data = remove(input_data)
    except Exception as e:
        print(f"Error removing background: {e}")  # Debug statement
        return "Error removing background", 500

    # Create an in-memory bytes buffer for the output
    output_byte_arr = io.BytesIO()
    output_byte_arr.write(output_data)
    output_byte_arr.seek(0)  # Move to the beginning of the BytesIO buffer

    return send_file(output_byte_arr, as_attachment=True, download_name=f"no_background_{filename}")
