from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

driver = webdriver.Chrome()

with open(r"C:\Users\Computer\Downloads\shopsy_sarees.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Discount", "Original Price", "Final Price", "Rating", "Reviews"])

    for page in range(1, 6):
        print(f"Page {page} scraping...")
        seen = set()  # Har page pe naya seen set!
        
        try:
            driver.get(f"https://www.shopsy.in/sarees-online/pr?page={page}")
            time.sleep(6)

            # Auto Scroll
            for _ in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)

            products = driver.find_elements(By.CSS_SELECTOR, "div[class*='r-1habvw']")
            print(f"Products mile: {len(products)}")

            if len(products) == 0:
                print(f"Page {page} load nahi hua — 5 sec retry...")
                time.sleep(5)
                products = driver.find_elements(By.CSS_SELECTOR, "div[class*='r-1habvw']")

            count = 0
            for p in products:
                try:
                    lines = p.text.strip().split("\n")
                    if len(lines) >= 4:
                        title = lines[0]

                        try:
                            title_elem = p.find_element(By.CSS_SELECTOR, "a[aria-label]")
                            full_title = title_elem.get_attribute("aria-label")
                            if full_title:
                                title = full_title
                        except:
                            pass

                        if title in seen:
                            continue
                        seen.add(title)

                        discount = lines[1] if "off" in lines[1] else ""
                        orig     = lines[2] if discount else ""
                        final    = lines[3] if discount else lines[2]

                        rating  = ""
                        reviews = ""
                        for line in lines:
                            line = line.strip()
                            try:
                                val = float(line)
                                if 1.0 <= val <= 5.0:
                                    rating = line
                            except:
                                pass
                            if line.startswith("(") and line.endswith(")"):
                                inner = line[1:-1]
                                if inner.isdigit():
                                    reviews = inner

                        writer.writerow([title, discount, orig, final, rating, reviews])
                        count += 1
                except:
                    pass

            print(f"Page {page} done! {count} products saved!")

        except Exception as e:
            print(f"Page {page} error: {e} — skip!")
            continue

driver.quit()
print("Saari pages complete!")