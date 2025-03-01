from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, auth, firestore
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")  # Ensure your HTML is inside a "templates" folder
CORS(app)  # Enable CORS

# 🔥 Load Firebase Admin SDK credentials
cred = credentials.Certificate("serviceAccountKey.json")  # Ensure this file is in your project folder
firebase_admin.initialize_app(cred)
db = firestore.client()  # Firestore Database

# 📌 Serve the Signup Page
@app.route('/', methods=['GET'])
def home():
    return render_template('signup.html')  # Serve the frontend

# 📌 Signup Route (Register User in Firebase Auth)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return jsonify({"message": "Please send a POST request with user data."})
    
    try:
        data = request.json
        if not all(key in data for key in [ "username","email", "password"]):
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
            "username": data["username"],
            "email": data["email"],
            "uid": user.uid
        })

        return jsonify({"message": "User registered successfully!", "uid": user.uid}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
