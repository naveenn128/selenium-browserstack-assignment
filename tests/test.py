import json
import time
import requests
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from deep_translator import GoogleTranslator
import yaml

# Load BrowserStack credentials and capabilities from YAML file
with open("browserstack.yml", "r", encoding="utf-8") as yml_file:
    config = yaml.safe_load(yml_file)

BROWSERSTACK_USERNAME = config["userName"]
BROWSERSTACK_ACCESS_KEY = config["accessKey"]
BROWSERSTACK_CAPABILITIES = config["platforms"]

def run_test(capability):
    """Run the test on a specific browser/device in BrowserStack."""
    options = ChromeOptions()
    options.set_capability("bstack:options", capability)
    options.set_capability("browserstack.username", BROWSERSTACK_USERNAME)
    options.set_capability("browserstack.accessKey", BROWSERSTACK_ACCESS_KEY)
    options.set_capability("sessionName", "El Pais Scraper Test")
    
    driver = webdriver.Remote(
        command_executor="https://hub-cloud.browserstack.com/wd/hub",
        options=options
    )

    try:
        # Open website
        driver.get("https://elpais.com/")
        
        #  **Wait for 20 seconds after opening the URL**
        time.sleep(20)  

        # Handle cookie consent pop-up
        try:
            accept_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[id="didomi-notice-agree-button"]'))
            )
            driver.execute_script("arguments[0].click();", accept_button)
            print(" Cookie pop-up accepted.")
        except Exception as e:
            print(f" No cookie pop-up found or already accepted. Error: {e}")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # **Wait for 10 seconds before searching for "Opinion" section**
        time.sleep(10)  

        # Navigate to "Opinion" section
        try:
            opinion_section = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Opinión"))
            )
            opinion_section.click()
            print(" Clicked on 'Opinión' section.")
            time.sleep(2)
        except:
            print(" 'Opinión' section not found!")
            driver.quit()
            return
        
        # Extract first 5 articles
        articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]
        translator = GoogleTranslator(source='es', target='en')
        all_words = []
        
        for index, article in enumerate(articles):
            try:
                title_element = article.find_element(By.TAG_NAME, "h2")
                title = title_element.text.strip()
                if not title:
                    print(f"Skipping Article {index+1} (No title found)")
                    continue
                
                print(f"\n Article {index+1} Title (Spanish): {title}")
                
                # Translate title
                translated = translator.translate(title)
                print(f" Translated Title: {translated}")
                
                # Process words
                words = re.findall(r'\b\w+\b', translated.lower())
                all_words.extend(words)
                
                # Download cover image
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

        # Analyze translated headers
        word_count = Counter(all_words)
        print("\n Repeated Words in Translated Titles (Appearing More Than Twice):")
        for word, count in word_count.items():
            if count > 2:
                print(f" {word}: {count}")

        # Mark test as passed
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Test completed successfully!"}}'
        )
    except Exception as err:
        message = f'Exception: {err.__class__.__name__} {str(err)}'
        driver.execute_script(
            f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"failed", "reason": {json.dumps(message)} }} }}'
        )
    finally:
        driver.quit()

# Run tests in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(run_test, BROWSERSTACK_CAPABILITIES[:5])
