import logging
import os
import random
import time

import requests
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from app_data import *

load_dotenv()


class Idiot:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.full_name = None
        self.email = None
        self.intro = None
        self.random_include_name = random.randint(1, 2)
        self.random_include_greeting = random.randint(1, 4)
        self.random_query = random.randint(1, 41)
        if self.random_include_name == 1:
            self.include_name = True
        else:
            self.include_name = False
        if self.random_include_greeting == 1:
            self.include_greeting = True
        else:
            self.include_greeting = False

    def gen_name(self) -> str:
        self.first_name = random.choice(first_names)
        self.last_name = random.choice(last_names)
        self.full_name = self.first_name + " " + self.last_name

    def gen_email(self) -> str:
        first_stop = random.randint(2, len(self.first_name) - 1)
        first_part = self.first_name[2:first_stop]
        last_stop = random.randint(2, len(self.last_name) - 1)
        last_part = self.last_name[2:last_stop]
        connectors = ["-", "_", ".", ""]
        random_conn = random.choice(connectors)
        possible_email_domains = ["gmai1", "qmail", "yahooo", "hotmai1", "ao1"]
        random_email_domain = random.choice(possible_email_domains)
        random_num = ""
        has_random_int = random.randint(1, 3)
        if has_random_int > 1:
            random_num = str(random.randint(1, 1000))
        if random_num != 1:
            self.email = (
                first_part
                + random_conn
                + last_part
                + random_num
                + "@"
                + random_email_domain
                + ".com"
            )
        else:
            self.email = (
                first_part
                + random_conn
                + last_part
                + "@"
                + random_email_domain
                + ".com"
            )

    def gen_intro(self) -> str:
        random_intro = random.randint(1, 12)
        if self.include_name:
            match random_intro:
                case 1:
                    self.intro = f"Hello my name is {self.full_name}. "
                case 2:
                    self.intro = f"The name's {self.full_name} and "
                case 3:
                    self.intro = f"Hi {self.full_name} here "
                case 4:
                    self.intro = f"Hi this is ol {self.first_name} "
                case 5:
                    self.intro = f"Yo, this is {self.first_name} "
                case 6:
                    self.intro = f"Yo this is big {self.first_name} "
                case 7:
                    self.intro = f"Good evening. You are speaking to {self.full_name}. "
                case 8:
                    self.intro = f"My name is {self.full_name}. I am sure you have heard of me. The {self.last_name}s are quite established in this region. "
                case 9:
                    self.intro = f"Hello my name is {self.full_name}. "
                case 10:
                    self.intro = f"Hi my name is {self.full_name}. "
                case 11:
                    self.intro = f"{self.full_name} - "
                case 12:
                    self.intro = f"Hi {self.first_name} here "

        else:
            match random_intro:
                case 1:
                    self.intro = "Hello hope you are doing well. I was hoping I could ask you a question? "
                case 2:
                    time_measurement = random.choice(time_measurements)
                    self.intro = f"Hey hope you remember me, we met several {time_measurement} ago, haha. "
                case 3:
                    self.intro = "Hi, first of all I love your shoes! "
                case 4:
                    self.intro = "yoo lovin the kicks "
                case 5:
                    self.intro = "Hello! "
                case 6:
                    self.intro = "helllloooooooo! "
                case 7:
                    self.intro = "Hey fellas, "
                case 8:
                    time_measurement = random.choice(time_measurements)
                    self.intro = f"Hey we met several {time_measurement} ago. "
                case 9:
                    self.intro = "uwu - "
                case 10:
                    self.intro = "yo "
                case 11:
                    self.intro = "hey "
                case 12:
                    self.intro = "hello "

    def gen_query(self) -> str:
        match self.random_query:
            case 1:
                self.query = "do you have any shoes in size 16? I can fit into a woman's size 19 if that helps"
            case 2:
                random_shoe_part = random.choice(shoe_parts)
                self.query = f"What is your selection of shoes with {random_shoe_part} on them? thanks"
            case 3:
                random_color = random.choice(random_colors)
                random_shoe = random.choice(kind_of_shoes)
                self.query = (
                    f"Do you have any {random_shoe} in {random_color}? Much thanks"
                )
            case 4:
                random_color = random.choice(random_colors)
                self.query = f"How is your selection for things in {random_color}?"
            case 5:
                random_shoe_link = random.choice(weird_shoes_urls)
                self.query = f"I am wondering if you have anything like this? {random_shoe_link}. lmk"
            case 6:
                self.query = "Do you do the shoe engraving thing?"
            case 7:
                random_shoe = random.choice(kind_of_shoes)
                self.query = f"do you guys have anything like {random_shoe}?"
            case 8:
                self.query = "how do you get your foot in the shoe after you put in the shoe tree? I am a little confused as to how this works. thx"
            case 9:
                num = random.randint(1, 13)
                self.query = f"I signed up with {num} different accounts, but I can't use all my codes?"
            case 10:
                random_shoe = random.choice(kind_of_shoes)
                random_sports_team = random.choice(sports_teams)
                self.query = f"can you do {random_shoe} in {random_sports_team} colors?"
            case 11:
                random_choice_1 = random.choice(kind_of_shoes)
                random_choice_2 = random.choice(kind_of_shoes)
                random_choice_3 = random.choice(kind_of_shoes)
                self.query = f"can you do a {random_choice_1}, {random_choice_2}, {random_choice_3} mix?"
            case 12:
                random_shoe = random.choice(kind_of_shoes)
                self.query = f"help find - {random_shoe} :)"
            case 13:
                self.query = "I am looking for shoes with much comfort in little pay and very stylish"
            case 14:
                self.query = "how get foot out of shoe? am little stuck for while"
            case 15:
                random_animal = random.choice(random_animals)
                self.query = f"do you have any shoes made out of {random_animal}?"
            case 16:
                random_sports_team = random.choice(sports_teams)
                random_animal = random.choice(random_animals)
                self.query = f"do you have any shoes made out of {random_animal}? And can you do it in {random_sports_team} colors ???"
            case 17:
                self.query = "do these shoes come with bluetooth?"
            case 18:
                self.query = "are these shoes self cleaning? Do they come with a self cleaning option?"
            case 19:
                self.query = "can you make shoes that change color based on my mood"
            case 20:
                mens_size = random.randint(4, 18)
                woman_size = mens_size + 2
                self.query = f"do you sell shoes in {mens_size}s - I can fit in a womans {woman_size} as well"
            case 21:
                shoe_url = random.choice(store_links)
                self.query = f"does this come in mens? {shoe_url}"
            case 22:
                currency = random.choice(weird_currencies)
                self.query = f"do you accept {currency} as payment?"
            case 23:
                self.query = "do you sell golf shoes?"
            case 24:
                self.query = "do you sell any shoes that glow in the dark?"
            case 25:
                random_location = random.choice(random_locations)
                self.query = f"do you ship to {random_location}?"
            case 26:
                self.query = "why are my shoes so sticky?"
            case 27:
                self.query = "are the tassles on the shoe detachable? thx"
            case 28:
                self.query = (
                    "do you offer a veteran discount for veterans from other countries?"
                )
            case 29:
                self.query = "do you offer a student discount?"
            case 30:
                self.query = "do you offer a senior discount?"
            case 31:
                random_location = random.choice(show_locations)
                self.query = f"could you come do a trunk show in {random_location}?"
            case 32:
                self.query = 'What does the "J" stand for?'
            case 33:
                self.query = "are you product halal?"
            case 34:
                self.query = "are your shoes kosher?"
            case 35:
                self.query = "do you guys deliver?"
            case 36:
                shoe_url = random.choice(store_links)
                self.query = f"are these best in slot? {shoe_url}"
            case 37:
                self.query = "can your shoes be cleaned with bleach?"
            case 38:
                self.query = "do you have cosplay shoes?"
            case 39:
                self.query = "do you guys actually read these?"
            case 40:
                self.query = (
                    "if i supplied the leather... could you make the shoes out of it..."
                )
            case 41:
                self.query = "remember me fuckface?"
            case 42:
                self.query = "is it possible to only buy 1 shoe?"
            case 43:
                self.query = "does your store offer free WiFi?"
            case 44:
                self.query = "I am outside your store. can you let me in plz?"
            case 45:
                self.query = "do you know what you will have available in 2029"
            case 46:
                self.query = "do you guys cater?"
            case 47:
                self.query = "if only you knew how bad things really were"
            case 48:
                self.query = "Glow2:wave2: buying fancy boots"
            case 49:
                self.query = "I am in the mood for some: formal. men's. footwear."
            case 50:
                self.query = "your website makes my brain hurt O_O"
        return self.query


def submit_annyoing_msg(query: str, PatrickStar: Idiot) -> None:
    logging.basicConfig(level=logging.DEBUG)
    chrome_options = Options()

    # Disable these to test
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(os.getenv("URL"))
        time.sleep(6)

        modal_element = driver.find_element(
            By.CSS_SELECTOR, "div[aria-label='POPUP Form']"
        )
        x_btn = modal_element.find_element(
            By.CSS_SELECTOR, "button[aria-label='Close dialog']"
        )
        x_btn.click()
        time.sleep(3)

        chat_btn = driver.execute_script(
            """
            const parent = document.getElementById('ShopifyChat')
            const shadowRoot = parent.shadowRoot
            const chatBtn = shadowRoot.querySelectorAll('[aria-label="Chat window"]')[0]
            return chatBtn
            """
        )
        chat_btn.click()
        time.sleep(2)

        chat_textarea = driver.execute_script(
            """
            const parent = document.getElementById('ShopifyChat')
            const shadowRoot = parent.shadowRoot
            const textArea = shadowRoot.querySelector('textarea')
            return textArea
            """
        )

        chat_textarea.click()
        chat_textarea.clear()
        time.sleep(1)
        chat_textarea.send_keys(query)
        time.sleep(1)
        chat_submit_btn = driver.execute_script(
            """
            const parent = document.getElementById('ShopifyChat')
            const shadowRoot = parent.shadowRoot
            const submitBtn = shadowRoot.querySelector('button')
            return submitBtn
            """
        )

        chat_submit_btn.click()
        time.sleep(2)

        # Fill in the templated info below
        first_name_input = driver.execute_script(
            """
            const parent = document.getElementById('ShopifyChat')
            const shadowRoot = parent.shadowRoot
            const inputs = shadowRoot.querySelectorAll('input')
            const firstName = inputs[0]
            return firstName
            """
        )

        first_name_input.click()
        first_name_input.clear()
        time.sleep(1)
        first_name_input.send_keys(PatrickStar.first_name)
        time.sleep(1)

        last_name_input = driver.execute_script(
            """
            const parent = document.getElementById('ShopifyChat')
            const shadowRoot = parent.shadowRoot
            const inputs = shadowRoot.querySelectorAll('input')
            const lastName = inputs[1]
            return lastName
            """
        )

        last_name_input.click()
        last_name_input.clear()
        time.sleep(1)
        last_name_input.send_keys(PatrickStar.last_name)
        time.sleep(1)

        email_input = driver.execute_script(
            """
            const parent = document.getElementById('ShopifyChat')
            const shadowRoot = parent.shadowRoot
            const inputs = shadowRoot.querySelectorAll('input')
            const email = inputs[2]
            return email
            """
        )

        email_input.click()
        email_input.clear()
        time.sleep(1)
        email_input.send_keys(PatrickStar.email)
        time.sleep(1)

        contact_submit_btn = driver.execute_script(
            """
            const parent = document.getElementById('ShopifyChat')
            const shadowRoot = parent.shadowRoot
            const submitBtn = shadowRoot.querySelector('button[type="submit"].hover-effect-button')
            return submitBtn
            """
        )

        contact_submit_btn.click()
        time.sleep(2)

        logging.info("Job complete")
        time.sleep(6)
        driver.quit()

    except Exception as e:
        logging.error(f"Error: {e}")


def ping_ntfy(name: str, msg: str) -> None:
    logging.info("Pinging ntfy...")
    url = os.getenv("NTFY_URL")
    data = f"""patrick-star successfully run

{name}: {msg}"""
    headers = {"Tags": "heavy_check_mark,patrick-star,cron-job"}

    try:
        response = requests.post(url, data=data, headers=headers)
        logging.info(response.status_code)
    except Exception as e:
        logging.error(f"Error: {e}")


def ping_discord(name: str, msg: str) -> None:
    logging.info("Pinging Discord...")
    msg = f"{name}: {msg}"
    webhook_url = os.getenv("WEBHOOK")
    try:
        webhook = DiscordWebhook(url=webhook_url, content=msg)
        response = webhook.execute()
        logging.info(response.status_code)
    except Exception as e:
        logging.error(f"Error: {e}")


def time_to_annoy() -> None:
    PatrickStar = Idiot()
    to_lower_rand = random.randint(1, 3)
    PatrickStar.gen_name()
    PatrickStar.gen_email()

    if PatrickStar.include_greeting:
        PatrickStar.gen_intro()

    query = PatrickStar.gen_query()
    if PatrickStar.intro is not None:
        query = PatrickStar.intro + PatrickStar.query

    if to_lower_rand == 1:
        query.lower()

    submit_annyoing_msg(query, PatrickStar)
    logging.info(f"Query sent by {PatrickStar.full_name}: {PatrickStar.query}")
    ping_ntfy(PatrickStar.full_name, PatrickStar.query)
    ping_discord(PatrickStar.full_name, PatrickStar.query)


if __name__ == "__main__":
    time_to_annoy()
