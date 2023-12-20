from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pickle
import time
import os

driver = webdriver.Chrome()

def main():
    for file in os.listdir(os.getcwd()):  # Check cookie file in working path
        if ".pkl" in file:
            print("Found a cookie!")
            driver.get("https://scrap.tf")
            time.sleep(2)
            # Load all cookies for login to scrap.tf
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            scrap_raffles()
        else:
            generate_cookies()  # If doesn't have cookie file, generate new one


def generate_cookies():
    driver.get("https://scrap.tf")
    print("Write \"ready\" after logging into scrap.tf")
    while True:
        user_input = input().lower()
        if user_input == "ready":
            break
    pickle.dump(driver.get_cookies(), open(
        "cookies.pkl", "wb"))  # Writing in pickle file
    driver.quit()


raffle_links = []


def scrap_raffles():
    driver.get("https://scrap.tf/raffles")

    # Scroll down to load all raffles
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)

    # Parsing the raffles
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for raffles in soup.find_all("div", class_="panel-raffle"):
        link = raffles.find("a")["href"]  # Get all raffles link
        # If raffle ended that's mean you won that raffle
        if raffles.find("span", class_="raffle-state-ended"):
            print(f"This raffle you won: https://scrap.tf" + link)
        else:
            # Append to raffle_links
            raffle_links.append("https://scrap.tf" + link)

    # Check if you entered some of them
    for joined_raffles in soup.find_all("div", class_="panel-raffle raffle-entered"):
        links = joined_raffles.find("a")["href"]
        # Remove them from raffle_links
        raffle_links.remove("https://scrap.tf" + links)

    print(f"{len(raffle_links)} Raffle Found To Join")

    enter_raffles()


def enter_raffles():

    raffle_count = 1
    for link in raffle_links:
        driver.get(link)

        # Check the enter raffle button
        button_xpath = "//button[@rel='tooltip-free' and not(@id)]"
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))).click()  # Wait until the enter raffle button
        except Exception:
            # If something happen goes with the next link
            print(f"An error occurred on this link {link}")
            continue

        # Check raffle leave id to ensure you joined the raffle
        raffle_leave = (By.ID, "raffle-leave")
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(raffle_leave))  # Wait until the leave raffle
            print(f"Joined! {raffle_count}/{len(raffle_links)}: {link}")
            raffle_count += 1
            time.sleep(2.5)
        except Exception:
            # If something happen goes with the next link
            print(f"An error occurred on that link {link}")
            continue

    driver.quit()


if __name__ == "__main__":
    main()
