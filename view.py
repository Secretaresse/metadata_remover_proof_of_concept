from flask import render_template, request, Blueprint
from PIL import Image
from PIL.ExifTags import TAGS
from app import create_app, upload_folder, download_folder
import os


bp = Blueprint('view', __name__)

@bp.route("/", methods= ["GET", "POST"])
def home():
    return render_template("home.html")

@bp.route("/view", methods= ["GET", "POST"])
def view_metadata():
    app = create_app()
    filename = request.args.get("name")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # Open the image using PIL
    try:
        image = Image.open(file_path)
    except FileNotFoundError:
        return "Image not found", 404

    # Extract other basic metadata
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

    # Extract EXIF data
    exifdata = image.getexif()

    # Iterating over all EXIF data fields
    for tag_id in exifdata:
        # Get the tag name, instead of the human-unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # Decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        info_dict[tag] = data
    return render_template("view_metadata.html", metadata=info_dict)

@bp.route("/result")
def view_stripped_metadata():
    app = create_app()
    filename = request.args.get("name")
    file = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)

    # Open the image using PIL
    try:
        image = Image.open(file)
    except FileNotFoundError:
        return "Image not found", 404

    # Extract other basic metadata
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

    # Extract EXIF data
    exifdata = image.getexif()

    # Iterating over all EXIF data fields
    for tag_id in exifdata:
        # Get the tag name, instead of the human-unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # Decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        info_dict[tag] = data
    # g.filename = filename
    return render_template("download.html", metadata=info_dict)




