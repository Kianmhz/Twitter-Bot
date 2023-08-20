from playwright.sync_api import sync_playwright
import os
from time import sleep
import requests
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('MY_USERNAME')  # replace with your environment variable for username
PASSWORD = os.getenv('MY_PASSWORD')  # replace with your environment variable for password


with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="/Users/kianmhz/Library/Application Support/Google/Chrome/Profile 2",
        headless=False,
    )

    page = context.new_page()

    page.goto("https://twitter.com/compose/tweet")

    if "login" in page.url:
        page.fill("input[name='text']", USERNAME)

        page.click("span:has-text('Next')")

        page.wait_for_selector("input[name='password']").fill(PASSWORD)

        page.click("span:has-text('Log in')")

    def post_tweet(file_path):
        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist.")
        else:
            page.set_input_files("input[data-testid='fileInput']", file_path)
            sleep(2)
            page.click("span:has-text('Post')")
        
    post_tweet("/Users/kianmhz/Downloads/abol1.jpeg")

    sleep(200)
    
