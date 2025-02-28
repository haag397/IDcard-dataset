
from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from jdatetime import datetime as jdatetime
import os
import time

app = Flask(__name__)

# Font path (change if needed)
# FONT_PATH = "/usr/share/fonts/truetype/Yekan.ttf"  # Adjust if necessary
FONT_PATH = "/home/hasan/Yekan.ttf"  # Adjust if necessary

# Convert Gregorian date to Jalali (Shamsi)
def gregorian_to_jalali(gregorian_date_str):
    gregorian_date = jdatetime.strptime(gregorian_date_str, "%Y/%m/%d").togregorian()
    jalali_date = jdatetime.fromgregorian(date=gregorian_date)
    return jalali_date.strftime("%Y/%m/%d")

# Function to generate fake ID card
def generate_id_card(national_id, name, last_name, father_name, birth_date, expiry_date):
    # image_path = "cleaned_id_card.jpg"  # Replace with actual template path
    # image_path = "new_ids.jpg"  # Replace with actual template path
    image_path = "cl_id.jpg"  # Replace with actual template path

    image = cv2.imread(image_path)

    # Convert BGR to RGB (OpenCV to Pillow)
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)

    # Try loading font
    try:
        font = ImageFont.truetype(FONT_PATH, 40)
    except IOError:
        print("Font not found. Using default font.")
        font = ImageFont.load_default()

    # Convert dates to Jalali
    birth_date_jalali = gregorian_to_jalali(birth_date)
    expiry_date_jalali = gregorian_to_jalali(expiry_date)

    # Define text positions (adjust as needed)
    positions = {
        "national_id": (800, 210),
        "name": (830, 300),
        "last_name": (767, 380),
        "birth_date": (810, 460),
        "father_name": (880, 538),
        "expiry_date": (810, 612),
    }

    # Data to be printed on the ID card
    data = {
        "national_id": national_id,
        "name": name,
        "last_name": last_name,
        "birth_date": birth_date_jalali,
        "father_name": father_name,
        "expiry_date": expiry_date_jalali
    }

    # Write text on image
    for key, value in data.items():
        draw.text(positions[key], value, font=font, fill=(0, 0, 0))  # Black text

    # Create unique filename
    timestamp = int(time.time())
    filename = f"generate_id{timestamp}.jpg"
    output_path = os.path.join("generate_id", filename)
    
    # Ensure output directory exists
    os.makedirs("generate_id", exist_ok=True)
    
    # Save image
    image_pil.save(output_path, format="JPEG")

    return output_path

# Flask API Endpoint
@app.route('/generate_id', methods=['POST'])
def generate_id():
    try:
        # Get JSON data from request
        data = request.json
        national_id = data.get("national_id", "۳۱۰۲۳۳۹۲۷۹")
        name = data.get("name", "")
        last_name = data.get("last_name", "")
        father_name = data.get("father_name", "")
        birth_date = data.get("birth_date", "")
        expiry_date = data.get("expiry_date", "2032-03-18")

        # Generate ID card
        file_path = generate_id_card(national_id, name, last_name, father_name, birth_date, expiry_date)

        # Return generated file
        return send_file(file_path, mimetype='image/jpeg', as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)