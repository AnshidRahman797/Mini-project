import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Assign admin claim
uid = "Uh3h1kt5ncZZVbG9rRFQl1hZ6n42"
auth.set_custom_user_claims(uid, {"admin": True})
print(f"Admin claim set for user: {uid}")
