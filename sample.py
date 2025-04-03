from flask import Flask, request, jsonify, send_file
import firebase_admin
from firebase_admin import credentials, auth, firestore
from flask_cors import CORS

app = Flask(__name__)  # No need for templates folder
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for frontend requests

# 🔥 Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")  # Ensure this file exists
firebase_admin.initialize_app(cred)
db = firestore.client()  # Firestore Database

@app.route('/')
def home():
    return send_file("index.html")  # Ensure index.html is in the same folder as your Flask app
@app.route('/')

# Redirect to index.html after login
@app.route('/redirect-to-home')
def redirect_to_home():
    return redirect(url_for('home'))  # Redirect to the home function

# 📌 Serve the Signup Page
@app.route('/signup', methods=['GET'])
def signup_page():
    return send_file("signup.html")  # ✅ Ensure signup.html is in the same folder

@app.route('/styles-signup.css')  # ✅ Remove parentheses from the route
def serve_signup_css():
    return send_file("styles-signup.css")  # ✅ Ensure the filename matches exactly

# 📌 Handle Signup (Register User in Firebase Auth)
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        if not all(key in data for key in ["username", "email", "password"]):
            return jsonify({"error": "Missing required fields"}), 400
        
        username = data["username"]
        email = data["email"]
        password = data["password"]

        # 🛠 Create user in Firebase Authentication
        user = auth.create_user(
            display_name=username,
            email=email,
            password=password
        )

        # 🔹 Store User Details in Firestore
        db.collection('users').document(user.uid).set({
            "username": username,
            "email": email,
            "uid": user.uid
        })

        return jsonify({"message": "User registered successfully!", "uid": user.uid}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 📌 Serve the Login Page
@app.route('/login', methods=['GET'])
def login_page():
    return send_file("login.html")  # ✅ Ensure login.html is in the same folder

# 📌 Serve CSS Files
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
# 📌 Serve the Event Registration Form
@app.route('/createevent', methods=['GET'])
def serve_event_form():
    return send_file("createevent.html")  

# 📌 Handle Event Registration (POST Request)
@app.route('/createevent', methods=['POST'])
def register_event():
    try:
        # ✅ Get text data from request.form
        event_name = request.form.get("event_name")
        event_caption = request.form.get("event_caption")
        event_type = request.form.get("event_type")
        event_fee = request.form.get("event_fee")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        state = request.form.get("state")
        city = request.form.get("city")
        college = request.form.get("college")
        contact_email = request.form.get("contact_email")
        contact_number = request.form.get("contact_number")
        event_description = request.form.get("event_description")
        
        # ✅ Handle File Upload (Convert Image to Base64)
        event_image = request.files.get("event_image")
        if event_image:
            image_data = base64.b64encode(event_image.read()).decode('utf-8')  # 🔹 Convert to Base64
        else:
            image_data = None  # No image provided

        # ✅ Store event details in Firestore
        event_data = {
            "event_name": event_name,
            "event_caption": event_caption,
            "event_type": event_type,
            "event_fee": event_fee,
            "start_date": start_date,
            "end_date": end_date,
            "state": state,
            "city": city,
            "college": college,
            "contact_email": contact_email,
            "contact_number": contact_number,
            "event_description": event_description,
            "event_image_base64": image_data,  # ✅ Store image as Base64 string
        }

        event_ref = db.collection('events').add(event_data)  

        return jsonify({"message": "Event registered successfully!", "event_id": event_ref[1].id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # ✅ Running both signup & login on port 5000
