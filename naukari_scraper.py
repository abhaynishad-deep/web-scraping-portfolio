# ── 1. IMPORTS ──
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import random
import json      # ← checkpoint ke liye
import os        # ← checkpoint ke liye

# ── 2. CHROME SETUP ──
chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# ── 3. CHECKPOINT CHECK ── ← naya
if os.path.exists("checkpoint.json"):
    with open("checkpoint.json", "r") as f:
        data = json.load(f)
    results = data["results"]
    start_page = data["last_page"] + 1
    print(f"✅ Checkpoint mila! Page {start_page} se shuru")
else:
    results = []
    start_page = 1
    print("🆕 Fresh start — Page 1 se")

# ── 4. LOOP ──
for page in range(start_page, 3):
    try:
        url = f"https://www.naukri.com/python-developer-jobs-{page}"
        driver.get(url)
        time.sleep(random.uniform(4, 7))

        jobs = driver.find_elements(By.CSS_SELECTOR, "div.srp-jobtuple-wrapper")

        if not jobs:
            print(f"⚠️ Page {page} empty — skipping")
            continue

        for job in jobs:
            try:
                title = job.find_element(By.CSS_SELECTOR, "div.row1 h2 a").text.strip()
            except:
                continue  # title nahi mila — job skip

            try:
                company = job.find_element(By.CSS_SELECTOR, "div.row2 span.comp-dtls-wrap").text.strip()
            except:
                continue  # company nahi mili — job skip

            try:
                exp = job.find_element(By.CSS_SELECTOR, "div.row3 span.expwdth").text.strip()
            except:
                exp = "NA"

            try:
                salary = job.find_element(By.CSS_SELECTOR, "div.row3 span.sal").text.strip()
            except:
                salary = "Not Disclosed"

            try:
                location = job.find_element(By.CSS_SELECTOR, "div.row3 span.locWdth").text.strip()
            except:
                location = "NA"

            try:
                skills = job.find_element(By.CSS_SELECTOR, "div.row5 ul.tags-gt").text.strip()
            except:
                skills = "NA"

            try:
                posted = job.find_element(By.CSS_SELECTOR, "div.row6 span.job-post-day").text.strip()
            except:
                posted = "NA"

            results.append([title, company, exp, salary, location, skills, posted])

        print(f"✅ Page {page} done — {len(results)} jobs total")

        # ── 5. CHECKPOINT SAVE ── ← naya
        with open("checkpoint.json", "w") as f:
            json.dump({"last_page": page, "results": results}, f)

    except Exception as e:
        print(f"❌ Page {page} error: {e} — skipping")
        continue

# ── 6. DRIVER BAND KARO ──
driver.quit()

# ── 7. CSV SAVE ──
with open(r"C:\Users\Computer\Downloads\shopsy-scraper\naukri_jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Job Title", "Company", "Experience", "Salary", "Location", "Skills", "Posted"])
    writer.writerows(results)

# ── 8. CHECKPOINT DELETE ── ← naya
if os.path.exists("checkpoint.json"):
    os.remove("checkpoint.json")

print(f"🎉 Done! {len(results)} jobs scraped!")