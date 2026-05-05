import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
SEARCH_QUERY = "gym Karachi"
MAX_RESULTS = 50  # Target number of results
OUTPUT_FILE = "gyms_karachi.csv"

def setup_driver():
    """Initializes and returns a Chrome WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--lang=en")  # Ensure page loads in English
    
    # Initialize the driver using webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_google_maps():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    
    results_data = []
    
    try:
        # 1. Navigate directly to search results
        search_url = f"https://www.google.com/maps/search/{SEARCH_QUERY.replace(' ', '+')}?hl=en"
        print(f"Opening: {search_url}")
        driver.get(search_url)
        
        # 2. Handle Cookie Consent if it appears
        try:
            time.sleep(5)
            consent_selectors = [
                '//form//button[contains(@aria-label, "Accept")]',
                '//button[contains(@aria-label, "Accept")]',
                '//span[text()="Accept all"]/..'
            ]
            for selector in consent_selectors:
                buttons = driver.find_elements(By.XPATH, selector)
                if buttons:
                    buttons[0].click()
                    print("Cookie consent accepted.")
                    time.sleep(3)
                    break
        except:
            pass
        
        # 3. Wait for the feed to appear
        print("Waiting for results to load...")
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@role, "feed")]')))
        except:
            print("Feed not found, attempting to find results directly...")
        
        time.sleep(5)
        
        while len(results_data) < MAX_RESULTS:
            # Find the scrollable container
            try:
                results_container = driver.find_element(By.XPATH, '//div[contains(@role, "feed")]')
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_container)
            except:
                # Fallback scroll
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            
            time.sleep(3)
            
            # Find all business links (class hfpxzc)
            business_elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")
            print(f"Found {len(business_elements)} potential matches in view...")
            
            for element in business_elements:
                if len(results_data) >= MAX_RESULTS:
                    break
                
                try:
                    name = element.get_attribute("aria-label")
                    if not name or any(d['Business Name'] == name for d in results_data):
                        continue
                        
                    # Click to open details
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(3)
                    
                    # Extract Details using more robust selectors
                    details = {"Business Name": name, "Phone Number": "N/A", "Address": "N/A", "Website": "N/A", "Instagram Handle": "N/A"}
                    
                    # Look for address
                    try:
                        addr = driver.find_element(By.XPATH, '//button[contains(@data-item-id, "address")]//div[contains(@class, "fontBodyMedium")]').text
                        details["Address"] = addr
                    except: pass
                    
                    # Look for phone
                    try:
                        phone = driver.find_element(By.XPATH, '//button[contains(@data-item-id, "phone:tel")]//div[contains(@class, "fontBodyMedium")]').text
                        details["Phone Number"] = phone
                    except: pass
                    
                    # Look for website
                    try:
                        site = driver.find_element(By.XPATH, '//a[contains(@data-item-id, "authority")]').get_attribute("href")
                        details["Website"] = site
                        details["Instagram Handle"] = "Check Website"
                    except: pass

                    results_data.append(details)
                    print(f"Scraped ({len(results_data)}/{MAX_RESULTS}): {name}")
                    
                except:
                    continue
            
            # Break if no new elements are found or end of list reached
            if "reached the end of the list" in driver.page_source.lower():
                break
                
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # 4. Save to CSV
        if results_data:
            df = pd.DataFrame(results_data)
            df.to_csv(OUTPUT_FILE, index=False)
            print(f"\nSuccessfully saved {len(results_data)} results to {OUTPUT_FILE}")
        else:
            print("No data collected.")
            
        driver.quit()

if __name__ == "__main__":
    scrape_google_maps()
