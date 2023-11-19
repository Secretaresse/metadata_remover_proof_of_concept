from flask import request, jsonify, Blueprint, render_template, redirect, url_for, send_from_directory
import os
from PIL import Image
from werkzeug.utils import secure_filename
from app import create_app, allowed_extensions, upload_folder, download_folder
from PIL.ExifTags import TAGS

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


bp = Blueprint('handler', __name__)

@bp.route("/upload", methods=["GET", "POST"])
def upload_image():
    app = create_app()
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "No file part"})

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for("view.view_metadata", name=filename))
        else:
            return jsonify({"error": "Invalid file format. Allowed formats are: png, jpg, jpeg, webp"})
    else:
        return jsonify({"error": "Invalid request method"})

@bp.route("/remove", methods=["POST"])
def remove_metadata():
    app = create_app()
    if request.method == "POST":
        upload_filename = request.form.get("name")

        if not upload_filename:
            return jsonify({"error": "No filename provided"}), 400
        
        upload_file_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_filename)
        # Open the image using PIL
        try:
            # Open the image using PIL
            image = Image.open(upload_file_path)
            
            # Strip EXIF
            data = list(image.getdata())
            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.putdata(data)

            # Save the image without metadata
            download_file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], upload_filename)
            image_without_exif.save(download_file_path)
            
            # Close the image handler after saving
            image.close()
            return redirect(url_for("view.view_stripped_metadata", name=upload_filename))

        except FileNotFoundError:
            return jsonify({"error": "Image not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Error processing image: {str(e)}"}), 500
        
    return jsonify({"error": "Wrong request method"}), 405   


@bp.route("/download", methods=["POST"])
def download():
    app = create_app()
    filename = request.form.get("name")
    upload_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    download_file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    
    response = send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

    if os.path.exists(upload_file_path) and os.path.exists(download_file_path):
        os.remove(upload_file_path)
        os.remove(download_file_path)
    
    return response




@bp.route("/nextimage", methods=["POST"])
def nextimage():
    return render_template("home.html")
