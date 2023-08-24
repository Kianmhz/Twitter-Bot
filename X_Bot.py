from playwright.sync_api import sync_playwright
import os
from time import sleep
import requests
from random import choice, randint, uniform
from dotenv import load_dotenv
import re

load_dotenv()

USERNAME = os.getenv('MY_USERNAME')  # replace with your environment variable for username
PASSWORD = os.getenv('MY_PASSWORD')  # replace with your environment variable for password


with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="C:\\Users\\kianm\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 5",  # replace with your own profile path
        headless=False,
    )

    page = context.new_page()

    page.goto("https://twitter.com/compose/tweet")

    # Check if need to login
    if "login" in page.url:
        page.fill("input[name='text']", USERNAME)
        sleep(uniform(2, 5))

        page.click("span:has-text('Next')")
        sleep(uniform(2, 5))

        page.wait_for_selector("input[name='password']").fill(PASSWORD)
        sleep(uniform(2, 5))

        page.click("span:has-text('Log in')")

    def post_tweet(file_path):
        # Will post a tweet with the given file path
        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist.")
        else:
            page.set_input_files("input[data-testid='fileInput']", file_path)
            sleep(uniform(2, 5))
            page.click("span:has-text('Post')")

    def fetchPost():
        # Will pick random posts from the source and downloads it
        page.goto(f'https://t.me/meme/{randint(200, 800)}?embed=1&mode=tme')  # replace with your own source
        linkElement = page.wait_for_selector('a.tgme_widget_message_photo_wrap')  
        imageStyle = linkElement.get_attribute('style')  
        regexPattern = r"background-image:url\('(.*)'\)"  # regex pattern to extract the image url
        match = re.search(regexPattern, imageStyle)

        # Download the image
        response = requests.get(match.group(1))
        if response.status_code == 200:
            with open('image.jpg', 'wb') as file:  
                file.write(response.content)
        else:
            print('Failed to download the image')


    def follow():
        # Will randomly pick one of these below sources and then follow their n last followers
        follow_id_list = ["username1"]  # Replace with your list of usernames
        random_number = choice(range(len(follow_id_list)))

        page.goto(f"https://twitter.com/{follow_id_list[random_number]}/followers")
        sleep(uniform(10, 15))

        # Get all the follow buttons
        follow_buttons = page.query_selector_all("div[role='button'][aria-label^='Follow @']")
        num_to_follow = randint(1, 15)

        # Follow random number of accounts
        for button in range(num_to_follow):
            follow_buttons[button].click()
            sleep(uniform(2, 5))

        print(f"Followed {num_to_follow} accounts.")

    follow()

    sleep(5)
