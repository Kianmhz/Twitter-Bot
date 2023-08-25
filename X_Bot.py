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
        try:
            # Will post a tweet with the given file path
            if not os.path.exists(file_path):
                print(f"The file {file_path} does not exist.")
                return  # Exit the function if the file doesn't exist

            page.set_input_files("input[data-testid='fileInput']", file_path)
            sleep(uniform(2, 5))
            page.click("span:has-text('Post')")

        except Exception as e:
            # This will catch any general exception and print its message
            print(f"An error occurred while posting the tweet: {e}")


    def fetchPost():
        # Number of attempts to fetch a post
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                # Will pick random posts from the source and downloads it
                page.goto(f'https://t.me/channelID/{randint(45000,60000)}?embed=1&mode=tme')  # replace with your own source
                sleep(uniform(2, 5))

                # Check for image
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
                            return  # Successfully downloaded the image, exit function
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
                            return  # Successfully downloaded the video, exit function
                        else:
                            print('Failed to download the video')
                            return

                attempts += 1  # Increment the attempt counter

            except Exception as e:
                # Handle any exception and print its message
                print(f"Attempt {attempts + 1} failed with error: {e}")
                attempts += 1  # Increment the attempt counter

        print("Failed to fetch a post after 3 attempts.")  # If reached here, all attempts were unsuccessful


    def follow():
        # Will randomly pick one of these below sources and then follow their n last followers
        follow_id_list = ["username1"]  # Replace with your list of usernames

        try:
            random_number = choice(range(len(follow_id_list)))
            page.goto(f"https://twitter.com/{follow_id_list[random_number]}/followers")
            sleep(uniform(10, 15))
        except Exception as e:
            print(f"Error navigating to the followers page: {e}")
            return

        try:
            # Get all the follow buttons
            follow_buttons = page.query_selector_all("div[role='button'][aria-label^='Follow @']")
            num_to_follow = randint(1, 15)
        except Exception as e:
            print(f"Error querying the follow buttons: {e}")
            return

        followed_count = 0  # To keep track of the number of successful follows

        # Follow random number of accounts
        for button in range(num_to_follow):
            try:
                follow_buttons[button].click()
                sleep(uniform(2, 5))
                followed_count += 1
            except Exception as e:
                print(f"Error following account number {button + 1}: {e}")

        print(f"Followed {followed_count} accounts.")

    
    def unfollow():
        try:
            # Navigate to the following page
            page.goto("https://twitter.com/username/following")
            sleep(uniform(10, 15))
        except Exception as e:
            print(f"Error navigating to the following page: {e}")
            return

        try:
            # Get all the unfollow buttons
            unfollow_buttons = page.query_selector_all("div[role='button'][aria-label^='Following @']")
            num_to_unfollow = randint(30, 70)
        except Exception as e:
            print(f"Error querying the unfollow buttons: {e}")
            return

        unfollowed_count = 0  # To keep track of the number of successful unfollows

        # Unfollow a random number of accounts
        for button in range(num_to_unfollow):
            try:
                unfollow_buttons[button].click()
                sleep(uniform(1, 2))
                page.wait_for_selector("div[role='button'] span:has-text('Unfollow')").click()
                sleep(uniform(2, 5))
                unfollowed_count += 1
            except Exception as e:
                print(f"Error unfollowing account number {button + 1}: {e}")

        print(f"Unfollowed {unfollowed_count} accounts.")




