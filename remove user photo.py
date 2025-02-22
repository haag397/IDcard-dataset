# import cv2
# import numpy as np
# import os
# from PIL import Image

# # Paths
# ID_CARD_PATH = "cleaned_id_card.jpg"  # Original ID card template
# REPLACEMENT_PHOTO_PATH = "sample.jpg"  # Photo to replace the original
# OUTPUT_PATH = "gnew_id_card.jpg"  # Output file

# # Define coordinates of the photo area (adjust based on template)
# PHOTO_TOP_LEFT = (10, 220)  # X, Y position (top-left corner)
# PHOTO_BOTTOM_RIGHT = (270, 420)  # X, Y position (bottom-right corner)

# def remove_and_replace_photo():
#     # Load ID card image
#     image = cv2.imread(ID_CARD_PATH)

#     # Create a mask for inpainting (cover the photo area)
#     mask = np.zeros(image.shape[:2], dtype=np.uint8)
#     cv2.rectangle(mask, PHOTO_TOP_LEFT, PHOTO_BOTTOM_RIGHT, 255, -1)

#     # Remove existing photo using inpainting
#     image_cleaned = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

#     # Load the replacement photo
#     replacement_photo = cv2.imread(REPLACEMENT_PHOTO_PATH)

#     # Resize the replacement photo to match the original size
#     width = PHOTO_BOTTOM_RIGHT[0] - PHOTO_TOP_LEFT[0]
#     height = PHOTO_BOTTOM_RIGHT[1] - PHOTO_TOP_LEFT[1]
#     replacement_resized = cv2.resize(replacement_photo, (width, height))

#     # Place the new photo in the cleaned area
#     image_cleaned[PHOTO_TOP_LEFT[1]:PHOTO_BOTTOM_RIGHT[1], PHOTO_TOP_LEFT[0]:PHOTO_BOTTOM_RIGHT[0]] = replacement_resized

#     # Save the output
#     cv2.imwrite(OUTPUT_PATH, image_cleaned)
#     print(f"Generated ID saved as {OUTPUT_PATH}")

# # Run function
# remove_and_replace_photo()


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
image = cv2.imread("cleaned_id_card.jpg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_pil = Image.fromarray(image_rgb)

# Clean text area
mask = np.zeros(image.shape[:2], dtype=np.uint8)
cv2.rectangle(mask, (80, 190), (600, 600), 255, -1)
image_cleaned = cv2.inpaint(image, mask, 2, cv2.INPAINT_TELEA)
image_pil_cleaned = Image.fromarray(cv2.cvtColor(image_cleaned, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(image_pil_cleaned)


# Save result
image_pil_cleaned.save("new_ids.jpg", quality=95)
print("ID card generated successfully!")


