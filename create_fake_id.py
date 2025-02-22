

from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from faker import Faker
import cv2
import numpy as np
from jdatetime import date as jdate

# Initialize Faker for Persian (Farsi) data
# fake = Faker('fa_IR')

# Specific values as requested
# fake_national_id = "۳۱۰۲۳۳۹۲۷۹"  # Persian numerals
# fake_name = "محمد"
# fake_last_name = "حسینی"
# fake_father_name = "علی"
# fake_birth_date = "1992-03-18"  # Gregorian date
# fake_expiry_date = "2032-03-18"  # Gregorian date

# Convert Gregorian dates to Jalali/Shamsi format with Persian numerals
# def gregorian_to_jalali(gregorian_date_str):
#     year, month, day = map(int, gregorian_date_str.split('-'))
#     jalali_date = jdate.fromgregorian(year=year, month=month, day=day)
#     return jalali_date.strftime("%Y/%m/%d").replace('0', '۰').replace('1', '۱').replace('2', '۲').replace('3', '۳').replace('4', '۴').replace('5', '۵').replace('6', '۶').replace('7', '۷').replace('8', '۸').replace('9', '۹')

# Convert dates
# fake_birth_date_jalali = gregorian_to_jalali(fake_birth_date)  # ۱۳۷۱/۰۱/۲۸
# fake_expiry_date_jalali = gregorian_to_jalali(fake_expiry_date)  # ۱۴۱۱/۰۱/۱۸

# Load and process image
image = cv2.imread("id_card.jpg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_pil = Image.fromarray(image_rgb)

# Clean text area
mask = np.zeros(image.shape[:2], dtype=np.uint8)
cv2.rectangle(mask, (710, 210), (1050, 645), 255, -1)
image_cleaned = cv2.inpaint(image, mask, 2, cv2.INPAINT_TELEA)
image_pil_cleaned = Image.fromarray(cv2.cvtColor(image_cleaned, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(image_pil_cleaned)

# Load Persian font (absolute path recommended)
# font = ImageFont.truetype("/usr/share/fonts/truetype/Yekan.ttf", 32)

# Text processing with proper RTL
# def process_text(text):
#     reshaped = arabic_reshaper.reshape(text)
#     return get_display(reshaped)

# Positions (adjust based on your template)
# positions = {
#     "national_id": (840, 220),
#     "name": (840, 300),
#     "last_name": (840, 380),
#     "birth_date": (840, 460),
#     "father_name": (840, 540),
#     "expiry_date": (840, 620),
# }

# Data to write
# data = {
#     "national_id": fake_national_id,
#     "name": fake_name,
#     "last_name": fake_last_name,
#     "birth_date": fake_birth_date_jalali,
#     "father_name": fake_father_name,
#     "expiry_date": fake_expiry_date_jalali
# }

# # Draw text
# for key, value in data.items():
#     draw.text(positions[key], process_text(value), font=font, fill=(0, 0, 0))

# Save result
image_pil_cleaned.save("generated_fake_ids.jpg", quality=95)
print("ID card generated successfully!")


