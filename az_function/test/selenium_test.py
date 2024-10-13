import re
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Firefox WebDriver
driver = webdriver.Firefox()

# URL of your static website
url = "https://ibtahajalifn.azurewebsites.net/api/http_triggerali?code=WPPoNdQGe5IGLeydRBoci53Qr2PNmWycwqEfseNfu_bSAzFuOq8ZGw%3D%3D"

# Open the website
driver.get(url)

try:
    # Wait for the visitor counter element to load
    counter_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "counter"))
    )

    # Get the initial visitor count and extract the numeric part
    text_with_count = counter_element.text
    match = re.search(r'\d+', text_with_count)

    if match:
        initial_count = int(match.group())
        print(f"Initial Visitor Count: {initial_count}")
    else:
        print("No visitor count found in the text.")
        driver.quit()
        exit(1)  # Exit if no count found

    # Refresh the page
    driver.refresh()

    # Wait again for the counter to load
    new_counter_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "counter"))
    )

    text_with_new_count = new_counter_element.text
    match = re.search(r'\d+', text_with_new_count)

    if match:
        new_count = int(match.group())
        print(f"New Visitor Count: {new_count}")
    else:
        print("No new visitor count found in the text.")
        driver.quit()
        exit(1)  # Exit if no count found

    # Check if the count has increased
    if new_count > initial_count:
        print("Test Passed: Visitor count incremented.")
    else:
        print("Test Failed: Visitor count did not increment.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the browser
    driver.quit()
