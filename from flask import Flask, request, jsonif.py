from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import pandas as pd
from jdatetime import datetime as jdatetime
import os
import time

app = Flask(__name__)

# Font path (change if needed)
FONT_PATH = "/usr/share/fonts/truetype/Yekan.ttf"  # Adjust if necessary
TEMPLATE_PATH = "new_ids.jpg"  # Your ID card template

# Convert Gregorian date to Jalali (Shamsi)
def gregorian_to_jalali(gregorian_date_str):
    try:
        gregorian_date = jdatetime.strptime(gregorian_date_str, "%Y-%m-%d").togregorian()
        jalali_date = jdatetime.fromgregorian(date=gregorian_date)
        return jalali_date.strftime("%Y/%m/%d")
    except:
        return gregorian_date_str  # Return as is if conversion fails

# Function to generate a single ID card
def generate_id_card(national_id, name, last_name, father_name, birth_date, expiry_date, output_folder):
    image = cv2.imread(TEMPLATE_PATH)
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)

    # Load font
    try:
        font = ImageFont.truetype(FONT_PATH, 40)
    except IOError:
        print("Font not found. Using default font.")
        font = ImageFont.load_default()

    # Convert dates to Jalali
    birth_date_jalali = gregorian_to_jalali(birth_date)
    expiry_date_jalali = gregorian_to_jalali(expiry_date)

    # Define text positions
    positions = {
        "national_id": (800, 210),
        "name": (950, 300),
        "last_name": (930, 380),
        "birth_date": (810, 460),
        "father_name": (950, 538),
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
    filename = f"{national_id}.jpg"
    output_path = os.path.join(output_folder, filename)

    # Save image
    os.makedirs(output_folder, exist_ok=True)
    image_pil.save(output_path, format="JPEG")

    return output_path

# Flask API for bulk processing
@app.route('/generate_bulk_ids', methods=['POST'])
def generate_bulk_ids():
    try:
        # Get CSV file from user request
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "CSV file is required"}), 400

        # Read CSV file into Pandas DataFrame
        df = pd.read_csv(file)

        # Check required columns
        required_columns = {"national_id", "name", "last_name", "father_name", "birth_date", "expiry_date"}
        if not required_columns.issubset(set(df.columns)):
            return jsonify({"error": f"CSV must contain columns: {required_columns}"}), 400

        output_folder = "generated_ids"
        generated_files = []

        # Generate ID cards for each row
        for _, row in df.iterrows():
            file_path = generate_id_card(
                row["national_id"], row["name"], row["last_name"], 
                row["father_name"], row["birth_date"], row["expiry_date"], output_folder
            )
            generated_files.append(file_path)

        return jsonify({"message": f"{len(generated_files)} ID cards generated!", "output_folder": output_folder})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
