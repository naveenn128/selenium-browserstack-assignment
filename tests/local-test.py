from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from deep_translator import GoogleTranslator
import requests
import os
import time
import re
from collections import Counter

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open website
url = "https://elpais.com/"
driver.get(url)
time.sleep(2)

# Navigate to the "Opinion" section
try:
    opinion_section = driver.find_element(By.LINK_TEXT, "Opinión")
    opinion_section.click()
    time.sleep(2)
except:
    print(" 'Opinión' section not found!")
    driver.quit()
    exit()

# Extract first 5 articles
articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]
translator = GoogleTranslator(source='es', target='en')
translated_titles = []
all_words = []

for index, article in enumerate(articles):
    try:
        # Get title
        title_element = article.find_element(By.TAG_NAME, "h2")
        title = title_element.text.strip()
        if not title:
            print(f" Skipping Article {index+1} (No title found)")
            continue

        print(f"\n Article {index+1} Title (Spanish): {title}")
        
        # Translate title
        translated = translator.translate(title)
        print(f" Translated Title: {translated}")
        translated_titles.append(translated)

        # Process words
        words = re.findall(r'\b\w+\b', translated.lower())
        all_words.extend(words)

        # Get cover image
        try:
            img_element = article.find_element(By.TAG_NAME, "img")
            img_url = img_element.get_attribute("src")
            if img_url:
                img_data = requests.get(img_url).content
                with open(f"article_{index+1}.jpg", "wb") as img_file:
                    img_file.write(img_data)
                print(f" Cover image downloaded for Article {index+1}")
        except:
            print(" No cover image found.")

    except Exception as e:
        print(f" Error processing Article {index+1}: {e}")

# Word Analysis
word_count = Counter(all_words)

# Print repeated words
print("\n🔍 Repeated Words in Translated Titles (Appearing More Than Twice):")
for word, count in word_count.items():
    if count > 2:
        print(f"{word}: {count}")

# Close the browser
driver.quit()
