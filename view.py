# This file is owned by: Jelle Groot
# Student Cyber Security
# University of Applied Sciences
# Project Security year 2

from flask import render_template, request, Blueprint
from PIL import Image
from PIL.ExifTags import TAGS
from app import create_app, upload_folder, download_folder
import os


bp = Blueprint('view', __name__)

@bp.route("/", methods= ["GET", "POST"])
def home():
    return render_template("home.html")

# Function to show the metadata
@bp.route("/view", methods= ["GET", "POST"])
def view_metadata():
    app = create_app()
    filename = request.args.get("name")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # Open the image
    try:
        image = Image.open(file_path)
    except FileNotFoundError:
        return "Image not found", 404

    # Extract the basic metadata
    info_dict = {
        "Filename": filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    for label, value in info_dict.items():
        print(f"{label:25}: {value}")

    # Extract the EXIF metadata
    exifdata = image.getexif()

    # Put all the fields in info_dict
    for tag_id in exifdata:
        # Get the tag name
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # Decode the EXIF data from the tag_id
        if isinstance(data, bytes):
            data = data.decode()
        info_dict[tag] = data
    return render_template("view_metadata.html", metadata=info_dict)


# Function to show the remaining metadata after stripping
@bp.route("/result")
def view_stripped_metadata():
    app = create_app()
    filename = request.args.get("name")
    file = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)

    # Open the image 
    try:
        image = Image.open(file)
    except FileNotFoundError:
        return "Image not found", 404

    # Extract the basic metadata
    info_dict = {
        "Filename": filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    for label, value in info_dict.items():
        print(f"{label:25}: {value}")

    # Extract EXIF metadata
    exifdata = image.getexif()

    # Put all the fields in info_dict
    for tag_id in exifdata:
        # Get the tag name
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # Decode the EXIF data from the tag_id
        if isinstance(data, bytes):
            data = data.decode()
        info_dict[tag] = data
    return render_template("download.html", metadata=info_dict)




