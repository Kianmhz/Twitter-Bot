from playwright.sync_api import sync_playwright
import os
from time import sleep
import requests
from random import choice
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

    def dataset():
        page.goto('https://t.me/meme/756')
        sleep(5)
        link_element = page.wait_for_selector('xpath=/html/body/div/div[2]/a[2]')
        print(link_element)
        image_style = link_element.get_attribute('style')
        image_url = image_style.split("url('")[1].split("')")[0]

        response = requests.get(image_url)
        if response.status_code == 200:
            with open('image.jpg', 'wb') as file:
                file.write(response.content)
        else:
            print('Failed to download the image')


    def follow_process():
        # Will randomly pick one of these below sources and then follow their n last followers
        follow_id_list = ["@dillondanis"]  # Replace with your list of usernames
        random_number = choice(range(len(follow_id_list)))

        # Open a new page
        page.goto(f"https://twitter.com/{follow_id_list[random_number]}/followers")
        sleep(30)

        # Start following
        acc = 1
        followed = 0
        errors = 0

        try:
            page.click(f'/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[{acc}]/div/div/div/div[2]/div[1]/div[2]/div')
        except:
            pass

        while followed != 20:
            try:
                sleep(1)
                acc += 1
                page.wait_for_selector(f'/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[{acc-2}]/div/div/div/div[2]/div[1]/div[2]/div')
                page.click(f'/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[{acc}]/div/div/div/div[2]/div[1]/div[2]/div')
                followed += 1
            except:
                errors += 1
                if errors >= 8:
                    break
                if page.is_visible('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[3]/div[1]'):
                    page.click('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[3]/div[1]')
                    sleep(4)

    follow_process()    

    sleep(200)
    
