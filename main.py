from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        StaleElementReferenceException,
                                        NoSuchElementException)
from random import randint
import time
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

LINKEDIN_LOGIN = "https://www.linkedin.com/login"
LINKEDIN_JOBS = ("https://www.linkedin.com/jobs/search/example_job")

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


def wait(minimum=300, maximum=600):
    time.sleep(randint(minimum, maximum) / 100)


# --------------------------------------------- LinkedIn Authentication ---------------------------------------------- #
driver.get(LINKEDIN_LOGIN)
wait()
for char in USERNAME:
    wait(minimum=5, maximum=10)
    driver.find_element(By.ID, value="username").send_keys(char)
wait()
for char in PASSWORD:
    wait(minimum=5, maximum=10)
    driver.find_element(By.ID, value="password").send_keys(char)
wait()
driver.find_element(By.XPATH, value="//*[@id='organic-div']/form/div[3]/button").click()

# --------------------------------------------- Application Bot ------------------------------------------------------ #

input("Press ENTER after solving the CAPTCHA")

driver.get(LINKEDIN_JOBS)
wait()
# job_list = driver.find_element(By.CSS_SELECTOR, value="ul.scaffold-layout__list-container")
# listing = job_list.find_elements(By.CSS_SELECTOR, value="li.scaffold-layout__list-item")
listing = driver.find_elements(By.CLASS_NAME, value="jobs-search-results__list-item")
for job in listing:
    print("Opening Listing")
    actions = ActionChains(driver)
    actions.move_to_element(job).perform()
    job.click()
    wait()
    try:
        easy_apply = driver.find_element(By.CSS_SELECTOR, value=".jobs-apply-button--top-card button")
        easy_apply.click()
        wait()
        first_next = driver.find_element(By.CSS_SELECTOR, value="footer div button")
        first_next.click()
        wait()
        second_next = driver.find_elements(By.CSS_SELECTOR, value="footer div button")[1]
        second_next.click()
        wait()
        submit = driver.find_elements(By.CSS_SELECTOR, value="footer div button")[1]
        if submit.text != "Submit application":
            raise ElementClickInterceptedException
        else:
            submit.click()

    # Handle cases where submitting is not one-step
    except ElementClickInterceptedException:
        try:
            wait()
            X_button = driver.find_element(By.CSS_SELECTOR, value="button")
            X_button.click()
            wait()
            lower_bar = driver.find_element(By.CSS_SELECTOR, value=".artdeco-modal__actionbar")
            lower_bar.find_elements(By.CSS_SELECTOR, value="button")[0].click()
            continue

        # Handle elements missing no longer available in the DOM
        except StaleElementReferenceException:
            continue

    # Exception just for testing purposes
    except NoSuchElementException:
        continue
wait()
driver.quit()
