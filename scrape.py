import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode, optional
service = Service('C:/Selenium Drivers/chromedriver-win64/chromedriver.exe')  # Update path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)


# Open the website
url = "https://www.serebii.net/pokemon/nationalpokedex.shtml"
driver.get(url)

# Find all elements containing Pokémon names
pokemon_elements = driver.find_elements(By.XPATH, "//td[@class='fooinfo']/a")

print("made 1")

# Extract the text from each element and store it in a list
pokemon_names = [element.text for element in pokemon_elements if element.text]


print("made 2")
# Close the WebDriver
driver.quit()

csv_file = 'pokemon_names.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Pokemon Name'])  # Write header
    for name in pokemon_names:
        writer.writerow([name])

print(f'Pokémon names have been written to {csv_file}')

