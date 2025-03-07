from flask import Flask, request, jsonify, send_file
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS

app = Flask(__name__)  
CORS(app)  

# 🔥 Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")  
firebase_admin.initialize_app(cred)  # ❌ Removed Firebase Storage
db = firestore.client()  # ✅ Firestore Database

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
        
        # ✅ Handle File Upload (Only Store Image Filename)
        event_image = request.files.get("event_image")
        image_filename = event_image.filename if event_image else None  # 🔹 Save filename instead of uploading

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
            "event_image_filename": image_filename,  # 🔹 Store filename instead of URL
        }

        event_ref = db.collection('events').add(event_data)  

        return jsonify({"message": "Event registered successfully!", "event_id": event_ref[1].id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================= RUN FLASK SERVER ========================= #

if __name__ == '__main__':
    app.run(debug=True, port=5000)  
