from flask import Flask
import os
import secrets

allowed_extensions = {"png", "jpg", "jpeg", "webp"}
upload_folder = 'uploads'
download_folder = 'downloads'

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    import view, handler 
    app.secret_key = secrets.token_urlsafe(32)


    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, upload_folder)
    app.config['DOWNLOAD_FOLDER'] = os.path.join(app.instance_path, download_folder)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(view.bp)
    app.register_blueprint(handler.bp)

    return app 


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host="0.0.0.0", port=port)



