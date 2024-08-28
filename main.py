from selenium import webdriver
import time
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()

profile_name = "pritesh-soni-0bbb291b1"

driver.get('https://www.linkedin.com/login')

email_field = driver.find_element("id",'username')
password_field = driver.find_element("id",'password')

email_field.send_keys('linkedin-email')
password_field.send_keys('linkedin-password')
password_field.submit()

driver.get(f"https://www.linkedin.com/in/{profile_name}/")  # Replace with the actual URL of the profile
time.sleep(5)

try:
    contact_info_button = driver.find_element("id", 'top-card-text-details-contact-info')
    contact_info_button.click()
    time.sleep(3)

    screenshot_path = f"linkedin_{profile_name}.png"
    driver.save_screenshot(screenshot_path)
except Exception as e:
    print("An error occurred:", e)

from openai import OpenAI
import os
import base64

## Set the API key and model name
MODEL="gpt-4o-mini"
client = OpenAI(api_key="openai-key")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(f"linkedin_{profile_name}.png")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant that Analyze Given Image and find email ID of an User from That image and responds in Json format.{'email':'<email-id>'}"},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}"}
            }
        ]}
    ],
    temperature=0.0,
)

print(response.choices[0].message.content)