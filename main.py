import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920x1080")

# Initialize the WebDriver using WebDriver Manager to automatically handle driver versioning
driver = webdriver.Chrome()

# Define the URL
url = "https://nahlizenidokn.cuzk.cz/ZobrazObjekt.aspx?encrypted=NAHL~xX5N-k19ysgrlE9TfWPsWD7FitatAKMF6Xy60KzoxGgh6ZrH5jmqM7nd46a9Z9hdmcRHsyJ5f0y0Tq4E59FFQuWjiAo7liguhM6KenVJfRbNods4Eu-0EUxSZZAx5LqXHCY-iNbar_zmX2tD9LPADumYvO-Ta-Y2wJky_1vIKjYfR7LKJdtlfystAoyqOMjQL1Gg8mjEj7klSDdRQN1ZtzDG7Wrn4gCyBu2ca_ftsEtAwhwx6Sc7wJ_eqFy8zWlOJBScM5JXldqKnensIa5yrBKp6IuRjax8pJIh7NQwmNZPcNDbJy8dWvI4wpwIN5H2hv0oZDWpnp4cn5yvVMZPZw3HVgvLawEt2SH_thta2tY_SxIe2HOtE_j3cBvy8rudeCM5R_hDqn5jyZ2LTgj0wTTcr6-srzLaRLjFr8sqSj9BtguWmOquX7Lc_DquYkjBcmioiSrNEPo-Y3hk3YaWcsk3T3-IFsozyl1bNpkMPeat0O_-rTHkJD8gUXyvaChhsqa0OhnzUvTvXc3XfDFrB1AemUj_9PzDsGFMx2O8FLs="

# Function to extract key-value pairs from a table
def extract_table_data(table_element):
    rows = table_element.find_elements(By.TAG_NAME, "tr")
    table_data = {}
    for row in rows:
        tds = row.find_elements(By.TAG_NAME, "td")
        if len(tds) == 2:
            key = tds[0].text.strip()
            value = tds[1].text.strip()
            table_data[key] = value
    return table_data

# Function to extract data from the main page
def extract_data(driver):
    try:
        # Open the URL
        driver.get(url)

        # Wait for the page to load completely
        time.sleep(1)  # Adjust this based on your internet speed

        # Find the table containing the rows
        table_element = driver.find_element(By.XPATH, "//*[@id='content']/table[3]/tbody")
        
        # Find all the rows within the table
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        
        # Initialize a list to store the hrefs
        hrefs = []
        
        # Iterate through each row and extract hrefs from anchor tags
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            for td in tds:
                anchors = td.find_elements(By.TAG_NAME, "a")
                for anchor in anchors:
                    href = anchor.get_attribute("href")
                    if href:
                        hrefs.append(href)
        
        return hrefs
    except Exception as e:
        return str(e)

# Function to extract data from the links
def extract_link_data(driver, link):
    try:
        # Open the link
        driver.get(link)

        # Wait for the page to load completely
        time.sleep(2)  # Adjust this based on your internet speed

        # Find the table containing the rows
        table_element = driver.find_element(By.CSS_SELECTOR, "#content > div.vysledek--mapa > table > tbody")

        # Extract table data
        link_data = extract_table_data(table_element)
        
        return link_data
    except Exception as e:
        return str(e)

# Extract data from the main page
hrefs = extract_data(driver)

# Initialize a list to store the link data
link_data_list = []

# Iterate through each link and extract data
for i, href in enumerate(hrefs):
    link_data = extract_link_data(driver, href)
    link_data_list.append(link_data)

# Save the extracted data to a JSON file
with open("extracted_data.json", "w", encoding="utf-8") as json_file:
    data = {"data": link_data_list}
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Print a success message
print("Data extraction completed and saved to 'extracted_data.json'.")

# Close the WebDriver
driver.quit()
