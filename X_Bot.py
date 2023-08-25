from playwright.sync_api import sync_playwright
import os
from time import sleep, time
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
        page.goto(f'https://t.me/shitpost/{randint(45000,60000)}?embed=1&mode=tme')  # replace with your own source
        sleep(uniform(2, 5))

        picElement = page.query_selector('a.tgme_widget_message_photo_wrap')
        if picElement:
            imageStyle = picElement.get_attribute('style')  
            regexPattern = r"background-image:url\('(.*)'\)"  # Regex pattern to extract the image URL
            match = re.search(regexPattern, imageStyle)

            if match:
                # Download the image
                response = requests.get(match.group(1))
                if response.status_code == 200:
                    with open('image.jpg', 'wb') as file:  
                        file.write(response.content)
                else:
                    print('Failed to download the image')
            return

        # If no image, check for a video
        videoElement = page.query_selector('video.tgme_widget_message_video.js-message_video')
        if videoElement:
            videoURL = videoElement.get_attribute('src')

            if videoURL:
                # Download the video
                response = requests.get(videoURL)
                if response.status_code == 200:
                    with open('video.mp4', 'wb') as file:
                        file.write(response.content)
                else:
                    print('Failed to download the video')


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

    
    def unfollow():
        # Will unfollow random number of accounts to avoid hitting the follow limit
        page.goto("https://twitter.com/username/following")
        sleep(uniform(10, 15))

        # Get all the follow buttons
        unfollow_buttons = page.query_selector_all("div[role='button'][aria-label^='Following @']")
        num_to_unfollow = randint(30, 70)

         # Follow random number of accounts
        for button in range(num_to_unfollow):
            unfollow_buttons[button].click()
            sleep(uniform(1, 2))
            page.wait_for_selector("div[role='button'] span:has-text('Unfollow')").click()
            sleep(uniform(2, 5))

        print(f"Followed {num_to_unfollow} accounts.")

    unfollow()


