from dotenv import load_dotenv
import os
from pathlib import Path

# Tentukan path ke file .env di luar file ini
env_path = Path("../") / ".env"
load_dotenv(dotenv_path=env_path)
from encode import recognitionImage, verifikasi, recognition
from flask import Flask, jsonify, request

app = Flask(__name__)
# app.config['LOG_LEVEL'] = os.environ.get('APP_LOG_LEVEL', 'INFO').upper()
debugs = os.getenv("APP_LOG_LEVEL")
print(debugs)

@app.route('/api/recodFR', methods=['POST'])
def process_data():
    data = request.json
    fileName = data.get("fileName", "")
    userName = data.get("userName", "")
    result = {"fileName": fileName,"userName": userName}
    return jsonify(result)


if __name__ == "__main__":
    # debug = True if os.environ.get("DEBUG") == "True" else False
    app.run(debug=debugs, port=5000)

    # recognitionImage("user.jpg", "fakhry")
    # recognitionImage("budi.jpg", "budi")
    # recognitionImage("368856-IMG20200307201411.jpg", "xx")
    # verifikasi("budi.jpg", "fakhry")
    # verifikasi("uji.jpg", "fakhry")
    # recognition("368856-IMG20200307201411.jpg")
    # recognition("photobooth.png")