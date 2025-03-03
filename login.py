from flask import Flask, request, jsonify, render_template, send_file
import firebase_admin
from firebase_admin import credentials, auth
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)

# 🔥 Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")  # Ensure this file exists
firebase_admin.initialize_app(cred)

# 📌 Serve Login Page
@app.route('/login', methods=['GET'])
def login_page():
    return send_file("login.html")
   
@app.route('/styles-login.css')  
def serve_css():
    return send_file("styles-login.css")

# 📌 Login Route (Authenticate User)
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
       
        if not data:
            return jsonify({"error": "No data received"}), 400
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # 🔹 Firebase Authentication does NOT allow verifying passwords directly in Flask.
        # 🔹 Instead, the frontend should send an ID token after user logs in.
        id_token = data.get("idToken")

        if not id_token:
            return jsonify({"error": "Missing ID token"}), 400

        # 🔍 Verify Firebase ID Token
        decoded_token = auth.verify_id_token(id_token)
        user_email = decoded_token.get("email")

        return jsonify({"message": "Login successful!", "email": user_email}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True)
