from flask import Flask, request, jsonify, send_file
import firebase_admin
from firebase_admin import credentials, auth, firestore
from flask_cors import CORS
import base64
from flask import Flask, jsonify
import threading
import time
import random
import firebase_admin
import base64
import requests
from io import BytesIO
from firebase_admin import credentials, firestore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

app = Flask(__name__)  # No need for templates folder
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for frontend requests

# 🔥 Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")  # Ensure this file exists
firebase_admin.initialize_app(cred)
db = firestore.client()  # Firestore Database

INSTAGRAM_USERNAME = "jude.njuden69"
INSTAGRAM_PASSWORD = "rogers@13"


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

 # ✅ Running both signup & login on port 5000
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--disable-software-rasterizer")  
    chrome_options.add_argument("--disable-dev-shm-usage")  
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    chrome_options.headless = False  
    driver = uc.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def get_instagram_usernames():
    usernames_ref = db.collection('instagram_usernames')
    docs = usernames_ref.stream()
    return [doc.id for doc in docs]

def click_popup_button(possible_texts):
    for text in possible_texts:
        try:
            xpath = f"//button[contains(text(), '{text}')]"
            button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            button.click()
            print(f"✅ Clicked popup button with text: '{text}'")
            return True
        except:
            continue
    return False
def instagram_login(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
  
    user_input = driver.find_element(By.NAME, "username")
    user_input.send_keys(username)
    time.sleep(random.uniform(1, 6)) 

    pass_input = driver.find_element(By.NAME, "password")
    pass_input.send_keys(password)
    time.sleep(random.uniform(1, 5))

   
    pass_input.send_keys(Keys.RETURN)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1iyjqo2')]"))
    )

    time.sleep(15) 
    wait = WebDriverWait(driver, 15)
    if not click_popup_button(['Not now', 'Not Now', 'Save Info', 'Remind me later']):
        print("❌ 'Not now' button not found.")

# Try for "Never" (Notification pop-up)
    if not click_popup_button(['Never', 'Not now', 'No thanks']):
        print("❌ 'Never' button not found.")

    print("✅ Instagram login successful!")
    return True 
    scroll_and_like_posts(driver)
    
def scroll_and_like_posts(driver):
    wait = WebDriverWait(driver, 10)
    for _ in range(5):  
        try:
            posts = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//article//div[contains(@class, '_aagu')]"))
            )

            if not posts:
                print("⚠️ No posts found!")
                return

            post = random.choice(posts)
            
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", post)
            time.sleep(1) 

            like_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[aria-label="Like"]')))
            like_button.click()

            time.sleep(3)  

        except TimeoutException:
            print("⏳ Timeout waiting for posts.")
            break
        except StaleElementReferenceException:
            print("🔄 Stale element detected. Retrying...")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error liking post: {e}")
            time.sleep(1)

def scrape_instagram(driver, usernames):
    print(len(usernames))
    for u_name in usernames:
        sleep_time = random.uniform(10, 15)
        print(f"⏳ Waiting {sleep_time:.2f} seconds before navigating to the next user...")
        time.sleep(sleep_time)

        url = f"https://www.instagram.com/{u_name}/"
        print(f"✅ Navigating to {url}")
        driver.get(url)

        time.sleep(5)
        print("🔎 DEBUG: Printing first 500 characters of page source")
        print(driver.page_source[:500])

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, '_aagw')]"))
            )
            print("✅ Profile loaded successfully")
        except:
            print("❌ Error: Profile page did not load properly.")
            return []

        print("🔄 Starting to scrape posts...")

        if "checkpoint_required" in driver.page_source or "login" in driver.current_url:
            print("⚠️ Instagram is blocking requests. Try logging in or using a different IP.")
            return []

        time.sleep(random.uniform(5, 8))

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/p/')]"))
            )
        except:
            print("❌ Timeout waiting for posts to load.")
            return []

        posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
        print(f"🔍 Found {len(posts)} post elements.")

        if not posts:
            print("🔄 No posts found on first try. Scrolling more and retrying...")
            for _ in range(5):  
                driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(random.uniform(2, 4))
                posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
                if len(posts) > 0:
                    break

        if not posts:
            print("❌ Still no posts found. Instagram may have blocked scraping.")
            return []

        print(f"✅ Found {len(posts)} posts!")

        scraped_data = []
        
        for post in posts[:10]:  
            try:
                post_url = post.get_attribute("href")
                post.click()
                time.sleep(random.uniform(15, 20))

               
                username_elem = driver.find_elements(By.CSS_SELECTOR, "header a[href*='/']")
                username = username_elem[0].text.strip() if username_elem else "❌ Username not found"

                try:
                    caption_xpath_list = [
                        "//h1",
                        "//div[contains(@class, 'x1i10hfl')]/span",
                        "//div[contains(@class, '_a9zs')]/span",
                        "//div[contains(@class, '_aacl')]/span",
                        "//div[contains(@class, '_aagv')]/span",
                        "//div[contains(@class, 'x1lliihq')]/span",
                        "//div[contains(@class, 'x1gslohp')]/span",
                        "//div[contains(@class, 'x1a2a7pz')]/span",
                        "//div[contains(@class, 'x1jx94hy')]/span",
                        "//div[@role='dialog']//h1",
                        "//div[@role='dialog']//span",
                        "//div[@role='dialog']//div[contains(@class, 'x1i10hfl')]/span",
                        "//div[@role='dialog']//ul[contains(@class, '_a9zj')]//span"
                    ]

                    caption = None
                    wait = WebDriverWait(driver, 10)
                    for xpath in caption_xpath_list:
                        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
                        for elem in elements:
                            text = elem.text.strip()
                            if text:
                                caption = text
                                break
                        if caption:
                            break

                    if not caption:
                        caption = "❌ Caption not found"

                except Exception as e:
                    caption = "❌ Caption not found"


                image_elem= driver.find_elements(By.XPATH, "//article//img")
                image_url = image_elem[0].get_attribute("src") if image_elem else "❌ Image not found"
                
                
                if image_url != "❌ Image not found":
                    try:
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            image_base64 = base64.b64encode(BytesIO(response.content).read()).decode('utf-8')
                        else:
                            image_base64 = "❌ Image conversion failed"
                    except:
                        image_base64 = "❌ Image conversion failed"
                else:
                    image_base64 = "❌ Image not found"

                timestamp_elem = driver.find_elements(By.CSS_SELECTOR, "time")
                timestamp = timestamp_elem[0].get_attribute("datetime") if timestamp_elem else "Unknown Time"

                post_data = {
                    "username": username,
                    "caption": caption,
                    "image_base64": image_base64,
                    "timestamp": timestamp,
                    "post_url": post_url
                }

                scraped_data.append(post_data)

                driver.find_element(By.XPATH, "//body").send_keys(Keys.ESCAPE)
                time.sleep(random.uniform(2, 4))

            except Exception as e:
                print(f"❌ Error extracting post data: {e}")
                continue

        if scraped_data:
            try:
                batch = db.batch()
                for i, post_data in enumerate(scraped_data):
                    doc_ref = db.collection("instagram_posts").document(f"{u_name}_post_{i}")
                    batch.set(doc_ref, post_data)

                batch.commit()
                print("✅ Successfully stored scraped data in Firestore!")

            except Exception as e:
                print(f"❌ Error storing data in Firestore: {e}")
        scraped_data.clear()
        continue

def run_scraper():
    """Logs into Instagram and scrapes profiles in the list."""
    driver = setup_driver()  

    try:
        print("🔑 Logging into Instagram...")
        login_success = instagram_login(driver, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

        if not login_success:  
            print("❌ Login failed. Exiting scraper.")
            return  
        INSTAGRAM_USERNAMES = get_instagram_usernames()
        print("🔍 Starting scraping process...")
        scrape_instagram(driver, INSTAGRAM_USERNAMES)

    finally:
        driver.quit()  
        print("🚪 Browser closed.")  

@app.route('/run-scraper', methods=['GET'])
def scrape():
    thread = threading.Thread(target=run_scraper)
    thread.start()
    return jsonify({"message": "Scraping started!"}), 200
    
@app.route('/admin/add-profile', methods=['POST'])
def add_profile():
    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"error": "Username is required"}), 400

    new_username = data["username"].strip()
    if not new_username:
        return jsonify({"error": "Username cannot be empty"}), 400

    # Reference to the 'instagram_usernames' collection
    usernames_ref = db.collection('instagram_usernames')

    # Check if the username already exists
    if usernames_ref.document(new_username).get().exists:
        return jsonify({"error": "Profile already exists"}), 400

    # Add the new username
    usernames_ref.document(new_username).set({})
    return jsonify({"message": f"Profile '{new_username}' added successfully!"}), 200

# Example route to check current profiles
@app.route('/admin/current-profiles', methods=['GET'])
def get_profiles():
    usernames_ref = db.collection('instagram_usernames')
    docs = usernames_ref.stream()
    usernames = [doc.id for doc in docs]
    return jsonify({"profiles": usernames}), 200

@app.route('/admin/promote', methods=['POST'])
def promote_user():
    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"error": "Username is required"}), 400

    username = data["username"].strip()
    if not username:
        return jsonify({"error": "Username cannot be empty"}), 400

    # Query Firestore to get the user document with this username
    users_ref = db.collection("users")
    query = users_ref.where("username", "==", username).stream()
    user_record = None
    for doc in query:
        user_record = doc.to_dict()
        break

    if not user_record or "uid" not in user_record:
        return jsonify({"error": f"User with username '{username}' not found."}), 404

    uid = user_record["uid"]

    try:
        auth.set_custom_user_claims(uid, {"admin": True})
        return jsonify({"message": f"User '{username}' promoted to admin successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/remove-profile', methods=['POST'])
def remove_profile():
    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"error": "Username is required"}), 400

    username = data["username"].strip()
    if not username:
        return jsonify({"error": "Username cannot be empty"}), 400

    # Reference to the 'instagram_usernames' collection
    usernames_ref = db.collection('instagram_usernames')
    doc_ref = usernames_ref.document(username)

    # Check if the document exists
    if not doc_ref.get().exists:
        return jsonify({"error": "Profile not found"}), 404

    # Delete the document
    doc_ref.delete()
    return jsonify({"message": f"Profile '{username}' removed successfully!"}), 200

@app.route('/submit_verified_event', methods=['POST'])
def submit_verified_event():
    try:
        # Use request.form if sent from a normal HTML form; if sent as JSON use request.get_json()
        # For example, if your form uses POST without AJAX, it sends form data.
        data = request.form if request.form else request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Extract all fields; note that event_image_base64 should be sent as text (base64 string)
        event_name = data.get("event_name")
        event_caption = data.get("event_caption")
        event_type = data.get("event_type")
        event_fee = data.get("event_fee")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        state = data.get("state")
        city = data.get("city")
        college = data.get("college")
        contact_email = data.get("contact_email")
        contact_number = data.get("contact_number")
        event_description = data.get("event_description")
        event_image_base64 = data.get("event_image_base64")

        # Create event document data
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
            "event_image_base64": event_image_base64,
            "timestamp": firestore.SERVER_TIMESTAMP
        }

        # Store the event data into the 'verified_events' collection
        doc_ref = db.collection('verified_events').add(event_data)
        return jsonify({"message": "Event registered successfully!", "event_id": doc_ref[1].id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 

