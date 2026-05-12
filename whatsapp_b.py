"""
WhatsApp Broadcast Automation using Selenium
- Opens WhatsApp Web ONLY ONCE
- Sends image + caption
- Personalized captions
- Stable selectors for latest WhatsApp Web

Requirements:
    pip install selenium

IMPORTANT:
1. Chrome must already be installed
2. WhatsApp Web login required once
3. Replace IMAGE_PATH with your real image path
4. Replace phone numbers with valid WhatsApp numbers
"""

import os
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ─────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("broadcast_log.txt"),
        logging.StreamHandler()
    ]
)

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────

CONTACTS = [
    {"name": "Kavitha", "phone": "917358340203"},
    {"name": "Vicky", "phone": "916383781654"},
]

MESSAGE_TEMPLATE = (
    "Hi {name}!\n"
    "This is a broadcast message from our team."
)

# CHANGE THIS TO YOUR REAL IMAGE PATH
IMAGE_PATH = r"C:\Users\Boomika\Pictures\sample.jpg"

# Delay between contacts
DELAY_BETWEEN_MESSAGES = 10

# Chrome profile folder
CHROME_PROFILE_PATH = r"C:\selenium\chrome-profile"

# Chrome executable
CHROME_BINARY = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def personalise(template: str, name: str) -> str:
    return template.replace("{name}", name)

# ─────────────────────────────────────────────────────────────
# SELENIUM SETUP
# ─────────────────────────────────────────────────────────────

# Create profile folder if missing
if not os.path.exists(CHROME_PROFILE_PATH):
    os.makedirs(CHROME_PROFILE_PATH)

options = webdriver.ChromeOptions()

# Chrome binary
options.binary_location = CHROME_BINARY

# Keep WhatsApp logged in
options.add_argument(f"--user-data-dir={CHROME_PROFILE_PATH}")

# Stability options
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")

# Launch browser
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 40)

# ─────────────────────────────────────────────────────────────
# OPEN WHATSAPP WEB
# ─────────────────────────────────────────────────────────────

driver.get("https://web.whatsapp.com")

print("\nScan QR if needed...")
input("After WhatsApp Web loads completely, press ENTER...")

# ─────────────────────────────────────────────────────────────
# SEND FUNCTION
# ─────────────────────────────────────────────────────────────

def send_image_with_caption(phone, message, image_path):

    logging.info(f"Opening chat for {phone}")

    # Open chat
    url = f"https://web.whatsapp.com/send?phone={phone}"

    driver.get(url)

    # Wait for chat to load
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[contenteditable="true"]')
        )
    )

    time.sleep(5)

    # Click attachment button
    attach_btn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[title="Attach"]')
        )
    )

    attach_btn.click()

    time.sleep(2)

    # Upload image
    file_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[type="file"]')
        )
    )

    file_input.send_keys(os.path.abspath(image_path))

    # Wait for caption box
    caption_box = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[contenteditable="true"]')
        )
    )

    time.sleep(3)

    # Type caption
    caption_box.send_keys(message)

    time.sleep(2)

    # Send button
    send_btn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'span[data-icon="send"]')
        )
    )

    send_btn.click()

    logging.info(f"Sent successfully to {phone}")

# ─────────────────────────────────────────────────────────────
# BROADCAST LOOP
# ─────────────────────────────────────────────────────────────

def send_broadcast():

    total = len(CONTACTS)

    logging.info(f"Starting broadcast to {total} contacts")

    for idx, contact in enumerate(CONTACTS):

        name = contact["name"]
        phone = contact["phone"]

        message = personalise(MESSAGE_TEMPLATE, name)

        logging.info(f"[{idx+1}/{total}] Sending to {name}")

        try:
            send_image_with_caption(
                phone,
                message,
                IMAGE_PATH
            )

        except Exception as e:
            logging.error(f"Failed for {name}: {e}")

        if idx < total - 1:
            logging.info(
                f"Waiting {DELAY_BETWEEN_MESSAGES} seconds..."
            )
            time.sleep(DELAY_BETWEEN_MESSAGES)

    logging.info("Broadcast completed.")

# ─────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":

    send_broadcast()

    print("\nDone.")
    input("Press ENTER to close browser...")

    driver.quit()
