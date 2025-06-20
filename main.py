import hashlib
import json
import logging
import os
import random
import time

import diskcache as dc
import requests
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from app_data import *

load_dotenv()


class Cache:
    """Handles caching of queries and names using diskcache."""

    def __init__(self):
        """Initializes the Cache object and sets up the cache directory."""
        self.cache = dc.Cache("./cache")

    def close_conn(self):
        """Closes the cache connection."""
        self.cache.close()

    def create_key(self, query_type: str, query: str):
        """Creates a unique cache key based on query type and query string.

        Args:
            query_type (str): The type of the query (e.g., 'query', 'first_name').
            query (str): The query string or value to cache. This will be normalized (lowercased and stripped).

        Returns:
            str: A unique cache key.
        """
        normalized_query = query.lower().strip()
        key_data = {"query_type": query_type, "query": str(normalized_query)}
        key_str = json.dumps(key_data, sort_keys=True)
        hashed = hashlib.sha256(key_str.encode()).hexdigest()
        return f"{query_type}:{hashed}"

    def add_key(self, key) -> None:
        """Adds a key to the cache with a fixed expiration time (15 days)."""
        # 5 days
        time = 15 * 24 * 60 * 60
        self.cache.set(key, True, expire=time)
        self.close_conn()

    def check_if_key_exists(self, query_type: str, query: str) -> bool:
        """Checks if a key exists in the cache. Adds the key if it does not exist.

        Args:
            query_type (str): The type of the query.
            query (str): The query string or value to check. This will be normalized (lowercased and stripped).

        Returns:
            bool: True if the key exists, False otherwise.
        """
        normalized_query = query.lower().strip()
        key = self.create_key(query_type, normalized_query)
        try:
            with dc.Cache("./cache", timeout=5) as cache:
                does_exist = cache.get(key, retry=False)

                if does_exist is None:
                    self.add_key(key)
                    return False
                return True
        except Exception as e:
            self.close_conn()
            print(f"[Cache Error] Could not read from cache: {e}")
            return False

    def clean_cache(self):
        """Expires old cache entries."""
        self.cache.expire()

    # method to flush the cache - useful for testing
    def clear_cache(self):
        """Clears all entries from the cache. Useful for testing purposes."""
        self.cache.clear()


class Idiot:
    """Represents a randomly generated customer profile for submitting queries."""

    def __init__(self):
        """Initializes the Idiot object with randomization flags and empty fields."""
        self.first_name = None
        self.last_name = None
        self.full_name = None
        self.email = None
        self.intro = None
        self.random_include_name = random.randint(1, 2)
        self.random_include_greeting = random.randint(1, 4)
        self.random_query = None
        if self.random_include_name == 1:
            self.include_name = True
        else:
            self.include_name = False
        if self.random_include_greeting == 1:
            self.include_greeting = True
        else:
            self.include_greeting = False

    def gen_first_name(self) -> str:
        """Generates and sets a random first name from the list of first names."""
        self.first_name = random.choice(first_names)

    def gen_last_name(self) -> str:
        """Generates and sets a random last name from the list of last names."""
        self.last_name = random.choice(last_names)

    def gen_full_name(self) -> str:
        """Concatenates the first and last name to set the full name."""
        self.full_name = self.first_name + " " + self.last_name

    def gen_email(self) -> str:
        """Generates and sets a random email address based on the first and last name."""
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
        """Generates and sets a random introduction string, optionally including the name."""
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
                case 13:
                    self.intro = f"You sniveling worm. My name is {self.first_name}. Remember it."
                case 14:
                    old_name = self.first_name
                    self.gen_first_name()
                    self.intro = f"The names {old_name}, but you can call me {self.first_name} hehe."
                case 15:
                    self.intro = f"uhhh *gulps audibly* my n-name is - *nervously looks around* err, I am called {self.first_name}"

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
                case 13:
                    self.intro = "hallo "
                case 14:
                    self.intro = "evenin' guvnah "
                case 15:
                    self.intro = "uhhhhhh "

    def gen_random_query_num(self) -> str:
        """Generates and sets a random query number for selecting a query template."""
        self.random_query = random.randint(1, 89)

    def gen_query(self) -> str:
        """Generates and returns a random query string based on the selected query number."""
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
                self.query = "are your product halal?"
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
            case 51:
                self.query = "do you deliver on the Sabbath?"
            case 52:
                self.query = "do you deliver on the day after the Sabbath?"
            case 53:
                self.query = "listen, I'm not saying its your shoes, but I have been getting SOME since I started wearing these around the funeral home"
            case 54:
                self.query = "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm shoes :)"
            case 55:
                self.query = "can I do an exchange for something out of stock?"
            case 56:
                self.query = "can I get interest on my return amount :^)"
            case 57:
                self.query = (
                    "can you expedite the return on my expedited shipping exchange?"
                )
            case 58:
                mens_size = random.randint(4, 18)
                self.query = f"what size would you recommend for someone who only wears size {mens_size} Crocs?"
            case 59:
                self.query = "your shoes make my penis look small >=("
            case 60:
                self.query = "can I get an extra large expedited return exchange on my order for the amount in full?"
            case 61:
                self.query = "can I initialize the return ordered operation for an exchange that I have already attempt to remediate - figuratively speaking?"
            case 62:
                self.query = "id like to do a full complete revision of my submitted order invoice - for tax purposes"
            case 63:
                random_store = random.choice(bizarre_retailers)
                self.query = f"can I change my payment method, i accidentally put it all on my {random_store} card - thanks"
            case 64:
                self.query = "can you paint flames on my shoes? thx"
            case 65:
                self.query = "english no well, cart not help order pay rapido"
            case 66:
                self.query = (
                    "I am wondering if you ship orders in deliveries or is different?"
                )
            case 67:
                self.query = "review where? must review read and review"
            case 68:
                self.query = "mmm shoes :)"
            case 69:
                self.query = (
                    "please add dark mode to your website, that is what I would do"
                )
            case 70:
                self.query = "If I ever see you in the Falador bank again, let's just say. There's gonna be trouble"
            case 71:
                self.query = "Do you sell on the Grand Exchange? please?"
            case 72:
                self.query = "first: I buy shoes, then: I leave a shitty review. It's that simple"
            case 73:
                self.query = "do you offer any 'all terrain' shoes? I uh work in a particular line of work"
            case 74:
                random_product = random.choice(sticky_things)
                self.query = f"HELP - I accidentally spilled {random_product} on my new suede shoes. What do? I may have accidentally rubbed it in"
            case 75:
                self.query = "is Fitzpatrick a family name?"
            case 76:
                self.query = "if I were to wear two shoes on my hands and two shoes on my feet, what would you recommend as the size difference between the front paws and back ones? thanks"
            case 77:
                self.query = "awesome shoes! These are perfect for yardwork!"
            case 78:
                self.query = "got a riddle for ya: what has 3 legs in the morning, 3 legs in the afternoon, and 3 legs in the evening? Me when I'm wearing your shoes xD"
            case 79:
                self.query = "I would like to exchange footwear in a location of my choosing at time of your choice and in a currency of an agreed upon medium. Possible?"
            case 80:
                self.query = "english no good: I am endeavoring to discuss the process of commandeering a pair of your most exquisite footwear. How must I initiate a cordial discussion on such matters?"
            case 81:
                self.query = "does your store have a printer? I would like to stop by and use it."
            case 82:
                self.query = "war... war never changes"
            case 83:
                self.query = (
                    "patrolling the Mojave almost makes you wish for a nuclear winter"
                )
            case 84:
                self.query = "do you accept oversized novelty checks?"
            case 85:
                self.query = (
                    "do you make clown shoes? if not, why? that is what I would do"
                )
            case 86:
                newCustomer = Idiot()
                newCustomer.gen_first_name()
                newCustomer.gen_last_name()
                self.query = f'has a guy named "{newCustomer.first_name} {newCustomer.last_name}" been asking you questions? DO NOT TRUST him. A right proper, swindler that one.'
            case 87:
                self.query = "my wife's boyfriend was interested in a pair of your shoes, any suggestions?"
            case 88:
                self.random_proverb = random.choice(ancient_hawaiians)
                self.query = f'the ancient hawaiians always used to say "{self.random_proverb}" have a nice day'
            case 89:
                self.query = "do you think this is funny? Is this a game to you? I don't find this funny. At all."
            case 90:
                self.query = "do you sell trimmed versions of your shoes?"
            case 91:
                self.query = "I MAY OR MAY NOT HAVE GOTTEN A CLEAR, TRANLUSCENT, GLUE-LIKE SUBSTANCE ALL OVR THE LACES AND THEN *ACCIDENTALLY* LET IT DRY IN THE SUN!! HELP"
        return self.query


def submit_annyoing_msg(query: str, PatrickStar: Idiot) -> None:
    """Submits an annoying message to the Shopify chat widget using Selenium automation.

    Args:
        query (str): The message/query to send.
        PatrickStar (Idiot): The customer profile to use for the submission.
    """
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
    """Sends a notification to ntfy with the provided name and message.

    Args:
        name (str): The name to include in the notification.
        msg (str): The message content.
    """
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
    """Sends a notification to Discord with the provided name and message.

    Args:
        name (str): The name to include in the notification.
        msg (str): The message content.
    """
    logging.info("Pinging Discord...")
    webhook_url = os.getenv("WEBHOOK")
    msg = f"{name}: {msg}"
    try:
        webhook = DiscordWebhook(url=webhook_url, content=msg)
        response = webhook.execute()
        logging.info(response.status_code)
    except Exception as e:
        logging.error(f"Error: {e}")


def time_to_annoy() -> None:
    """Orchestrates the process of generating a random customer, query, and submitting it.

    This function ensures that the generated query, first name, and last name are unique (not in cache),
    then submits the message, and sends notifications via ntfy and Discord.
    """
    DiskCache = Cache()
    PatrickStar = Idiot()

    PatrickStar.gen_first_name()
    PatrickStar.gen_last_name()
    PatrickStar.gen_full_name()
    PatrickStar.gen_email()
    PatrickStar.gen_random_query_num()

    if PatrickStar.include_greeting:
        PatrickStar.gen_intro()

    query_attempts = 0
    while True:
        if PatrickStar.include_greeting:
            PatrickStar.gen_intro()  # Regenerate intro for more variety

        query = PatrickStar.gen_query()
        if PatrickStar.intro:
            query = PatrickStar.intro + query

        # Always normalize query before checking cache
        normalized_query = query.lower().strip()

        if not DiskCache.check_if_key_exists(
            query_type="query", query=normalized_query
        ):
            logging.info(
                f"Unique query found after {query_attempts + 1} attempt(s): {normalized_query}"
            )
            break
        else:
            logging.debug(
                f"Query already in cache, retrying. Attempt: {query_attempts + 1}"
            )
        PatrickStar.gen_random_query_num()
        query_attempts += 1

    first_name_attempts = 0
    while True:
        normalized_first_name = PatrickStar.first_name.lower().strip()
        if not DiskCache.check_if_key_exists(
            query_type="first_name", query=normalized_first_name
        ):
            logging.info(
                f"Unique first name found after {first_name_attempts + 1} attempt(s): {normalized_first_name}"
            )
            break
        else:
            logging.debug(
                f"First name already in cache, retrying. Attempt: {first_name_attempts + 1}"
            )
            PatrickStar.gen_first_name()
            first_name_attempts += 1

    last_name_attempts = 0
    while True:
        normalized_last_name = PatrickStar.last_name.lower().strip()
        if not DiskCache.check_if_key_exists(
            query_type="last_name", query=normalized_last_name
        ):
            logging.info(
                f"Unique last name found after {last_name_attempts + 1} attempt(s): {normalized_last_name}"
            )
            break
        else:
            logging.debug(
                f"Last name already in cache, retrying. Attempt: {last_name_attempts + 1}"
            )
            PatrickStar.gen_last_name()
            last_name_attempts += 1

    PatrickStar.gen_full_name()

    submit_annyoing_msg(query, PatrickStar)
    print(f"Query sent by {PatrickStar.full_name}: {query}")
    logging.info(f"Query sent by {PatrickStar.full_name}: {query}")
    ping_ntfy(PatrickStar.full_name, query)
    ping_discord(PatrickStar.full_name, query)

    # DiskCache.clear_cache() # for testing only
    DiskCache.clean_cache()


if __name__ == "__main__":
    time_to_annoy()
