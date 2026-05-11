from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import random

chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.99acres.com/search/property/buy/bangalore?city=20&preference=S&budget_min=0&res_com=R&isPreLeased=N"
driver.get(url)
time.sleep(4)

results = []
page = 1
max_pages = 100  # Test ke liye

while page <= max_pages:
    print(f"📄 Page {page} scraping...")
    time.sleep(random.uniform(3, 5))

    cards = driver.find_elements(By.CSS_SELECTOR, "div.PseudoTupleRevamp__outerTupleWrap")

    cards = driver.find_elements(By.CSS_SELECTOR, "div.PseudoTupleRevamp__outerTupleWrap")

    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "div.PseudoTupleRevamp__heading").text.strip()
        except:
            continue
        try:
            subtitle = card.find_element(By.CSS_SELECTOR, "h2.PseudoTupleRevamp__subHeading").text.strip()
        except:
            subtitle = "NA"
        try:
            price = card.find_element(By.CSS_SELECTOR, "div.configs__configCardsWrap").text.strip()
        except:
            price = "NA"
        try:
            location = card.find_element(By.CSS_SELECTOR, "div.tupleNew__scrollableNearby").text.strip()
        except:
            location = "NA"

        results.append([title, subtitle, price, location])

    print(f"✅ Page {page} done — {len(results)} properties")

    # Next button click karo
    try:
        next_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Next Page')]")
        driver.execute_script("arguments[0].click();", next_btn)
        page += 1
    except:
        print("Next button nahi mila — band karo")
        break

driver.quit()

with open(r"C:\Users\Computer\Downloads\shopsy-scraper\acres99_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Subtitle", "Price", "Location"])
    writer.writerows(results)

print(f"🎉 Done! {len(results)} properties!")