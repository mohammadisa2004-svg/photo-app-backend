from flask import Flask, request, jsonify
from flask_cors import CORS
from upload import upload_image  # Azure Blob upload function

app = Flask(__name__)
CORS(app)  # allow frontend from another region to call backend

@app.route('/')
def home():
    return "Photo App Backend is running"

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    try:
        blob_url = upload_image(file)
        return jsonify({"message": "Photo uploaded successfully!", "url": blob_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
