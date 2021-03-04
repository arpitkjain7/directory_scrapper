import os
import time
import names
import random
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


def get_basic_details(driver, idx):
    shop_name = driver.find_element_by_xpath(
        f"//div[@id='searchResults']/div[{idx}]/div[1]"
    ).text
    shop_city = driver.find_element_by_xpath(
        f"//div[@id='searchResults']/div[{idx}]/div[5]"
    ).text
    shop_state = driver.find_element_by_xpath(
        f"//div[@id='searchResults']/div[{idx}]/div[7]"
    ).text
    driver.find_element_by_xpath(
        f"//div[@id='searchResults']/div[{idx}]/div[10]/a/input"
    ).send_keys("\n")
    return shop_name, shop_city, shop_state


def get_phone_number(driver):
    try:
        view_phone_number_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[text()='View Phone Number']",
                )
            )
        )
        ActionChains(driver).move_to_element(view_phone_number_button).click(
            view_phone_number_button
        ).perform()
        # view_phone_number_button.send_keys("\n")
        form_name = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[text()='Fill this form with your correct details to view phone numbers']/following-sibling::input[@placeholder='Name']",
                )
            )
        )
        form_name.send_keys(names.get_full_name())
        form_email_id = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[text()='Fill this form with your correct details to view phone numbers']/following-sibling::input[@placeholder='Email Address']",
                )
            )
        )
        form_email_id.send_keys(f"raj_singh_{random.randint(1000,9999)}@gmail.com")
        form_phone_no = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[text()='Fill this form with your correct details to view phone numbers']/following-sibling::input[@placeholder='Phone']",
                )
            )
        )
        form_phone_no.send_keys(random.randint(8000000000, 9999999999))
        driver.find_element_by_xpath(
            "//span[text()='Fill this form with your correct details to view phone numbers']/following-sibling::input[@value='Submit']"
        ).send_keys("\n")
        shop_phone_number = []
        shop_phone_number_1 = driver.find_element_by_xpath(
            "//div[@id='phoneNumbers']/a"
        ).text
        print(shop_phone_number_1)
        shop_phone_number_2 = None
    except:
        pass
    try:
        shop_phone_number_2 = driver.find_element_by_xpath(
            "//div[@id='phoneNumbers']/a/following-sibling::a"
        ).text
        print(shop_phone_number_2)
    except:
        pass
    # for value in shop_phone_number_list:
    #     shop_phone_number.append(value.text)
    #     print(shop_phone_number)
    return shop_phone_number_1, shop_phone_number_2


def Extract_Data(search_param: str, batch_id: str, headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(
        "/Users/arpitkjain/Desktop/Data/POC/google_scrapper/chromedriver",
        chrome_options=options,
    )
    driver.get("https://www.deldure.com/")
    search_bar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//input[@placeholder='Search for Business Listing']",
            )
        )
    )
    search_bar.send_keys(search_param)
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//input[@placeholder='Search for Business Listing']/following-sibling::input",
            )
        )
    )
    search_button.send_keys("\n")
    time.sleep(5)
    search_result = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//div[@id='searchHeader']",
            )
        )
    )
    search_output = search_result.text
    shop_data = []
    print(search_output)
    isNext = True
    while isNext:
        url = driver.current_url
        for i in range(1, 13):
            shop_name, shop_city, shop_state = get_basic_details(driver, i)
            shop_phone_number_1, shop_phone_number_2 = get_phone_number(driver)
            shop_data.append(
                [
                    shop_name,
                    shop_city,
                    shop_state,
                    shop_phone_number_1,
                    shop_phone_number_2,
                    search_param,
                ]
            )
            # driver.back()
            driver.get(url)
            time.sleep(5)
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[text()='Next']",
                )
            )
        )
        next_button.send_keys("\n")
        time.sleep(5)
        try:
            driver.find_element_by_xpath(
                "//div[text()='Website search is under maintenance. We will be back in few minutes.']"
            )
            isNext = False
        except NoSuchElementException:
            print("Navigating to next page")
        print(f"{isNext=}")
        time.sleep(5)
        # print(f"{shop_data=}")
    driver.close()
    return shop_data
