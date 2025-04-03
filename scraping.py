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


app = Flask(__name__)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

INSTAGRAM_USERNAME = "jude.njuden69"
INSTAGRAM_PASSWORD = "rogers@13"
INSTAGRAM_USERNAMES = ["tinkerhub_gecpkd","iedcgecpkd","ieeesbgecpkd"]

def random_delay(min_time=2, max_time=5):
    time.sleep(random.uniform(min_time, max_time))

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--disable-software-rasterizer")  
    chrome_options.add_argument("--disable-dev-shm-usage")  
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    chrome_options.headless = False  
    driver = uc.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

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

    time.sleep(5) 
    try:
        not_now_button = driver.find_element(By.XPATH, "//button[text()='Not now']")
        not_now_button.click()
        print("Clicked 'Not now' button.")
    except:
        print("No 'Not now' button found.")

    try:
        never_button = driver.find_element(By.XPATH, "//button[text()='Never']")
        never_button.click()
        print("Clicked 'Never' button.")
    except:
        print("No 'Never' button found.")

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
        

def human_scroll(driver, min_scroll=2, max_scroll=5):
    """Simulates human-like scrolling behavior"""
    for _ in range(random.randint(min_scroll, max_scroll)):
        scroll_distance = random.randint(300, 800)
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(1.5, 3))

def human_mouse_movement(driver):
    """Simulates human-like mouse movements within browser window"""
    actions = ActionChains(driver)

    driver.maximize_window()
    time.sleep(2) 

    window_size = driver.get_window_size()
    max_x = window_size["width"] - 100  
    max_y = window_size["height"] - 100

    for _ in range(random.randint(3, 6)):  
        x = random.randint(10, max_x)
        y = random.randint(10, max_y)
        
        actions.move_by_offset(x - driver.get_window_rect()["x"], 
                               y - driver.get_window_rect()["y"]).perform()
        time.sleep(random.uniform(0.5, 1.5))  
def human_scroll(driver):
    for _ in range(random.randint(2, 4)):
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(random.uniform(2, 4))  

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
                time.sleep(random.uniform(3, 5))

               
                username_elem = driver.find_elements(By.CSS_SELECTOR, "header a[href*='/']")
                username = username_elem[0].text.strip() if username_elem else "❌ Username not found"

                try:
                    caption_xpath = (
                        "//h1 | "
                        "//div[contains(@class, 'x1i10hfl')]/span | "
                        "//div[contains(@class, '_a9zs')]/span | "
                        "//div[contains(@class, '_aacl')]/span | "
                        "//div[contains(@class, '_aagv')]/span | "
                        "//div[contains(@class, 'x1lliihq')]/span | "
                        "//div[contains(@class, 'x1gslohp')]/span | "
                        "//div[contains(@class, 'x1a2a7pz')]/span | "
                        "//div[contains(@class, 'x1jx94hy')]/span"
                    )

                    caption_elem = driver.find_element(By.XPATH, caption_xpath)
                    caption = caption_elem.text.strip() if caption_elem else "❌ Caption not found"
                except:
                    caption = "❌ Caption not found"


                image_elem = driver.find_elements(By.XPATH, "//img[contains(@class, 'x5yr21d')]")
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

                print("🔎 DEBUG: Extracted post data:", post_data)
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
