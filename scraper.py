# scraper.py
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Public list of filmhouse agenda pages scanned by the crawler.
FILMHOUSE_URLS = [
    "https://springhaver.nl/agenda/",
    "https://hartlooper.nl/agenda/",
    "https://slachtstraat.nl/agenda/"
]

def parse_movies(html, base_site):
    """
    Parse the HTML to extract movie titles and playing times with complete ticket links.
    Each movie will have:
      - 'title': the movie title,
      - 'playings': a list of dictionaries with:
            'time': playing time (text),
            'ticket_link': full URL to the ticket page.
    """
    soup = BeautifulSoup(html, 'html.parser')
    movies = []
    movie_tiles = soup.find_all(class_='tile__title')
    
    for tile in movie_tiles:
        a_tag = tile.find('a')
        title = a_tag.get_text(strip=True) if a_tag else tile.get_text(strip=True)
        
        playings = []
        for elem in tile.find_all_next():
            if elem.get("class") and "tile__title" in elem.get("class"):
                break
            if elem.name == "div" and "btn--schedule__time" in elem.get("class", []):
                span = elem.find("span")
                time_text = span.get_text(strip=True) if span else None
                parent_a = elem.find_parent("a")
                ticket_link = parent_a.get("href") if parent_a else None
                if time_text and ticket_link:
                    full_ticket_link = urljoin(base_site, ticket_link)
                    playings.append({
                        "time": time_text,
                        "ticket_link": full_ticket_link
                    })
        movies.append({
            "title": title,
            "playings": playings
        })
    return movies

def get_movies_for_week_by_dropdown(base_url):
    """
    Load the theater agenda once and use the date dropdown to collect movies for the week.
    Only processes options from the date filter and skips unwanted ones.
    Limits to the first 7 days.
    """
    options = Options()
    options.headless = True  # Set to False during testing if you want to see browser actions.
    # Use webdriver-manager to automatically download and manage the ChromeDriver
    # so contributors do not need to install chromedriver manually.
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(base_url)

    parsed = urlparse(base_url)
    base_site = f"{parsed.scheme}://{parsed.netloc}"
    
    # Wait for and click the date button.
    date_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.js-date-button"))
    )
    date_button.click()
    
    # Wait until at least one day option is present.
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.listbox[aria-labelledby='date_label'] li[role='option']"))
    )
    
    movies_by_day = {}
    day_options_elements = driver.find_elements(
        By.CSS_SELECTOR, 
        "ul.listbox[aria-labelledby='date_label'] li[role='option']"
    )
    day_options = []
    for option in day_options_elements:
        option_class = option.get_attribute("class")
        if "listbox-option--alldays" in option_class:
            continue
        day_text = option.text.strip()
        if not day_text:
            continue
        data_value = option.get_attribute("data-value")
        day_options.append((day_text, data_value))
    
    # Limit to the first 7 day options.
    day_options = day_options[:8]
    print("Filtered day options:", day_options)
    
    actions = ActionChains(driver)
    for day_text, data_value in day_options:
        date_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.js-date-button"))
        )
        date_button.click()
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.listbox[aria-labelledby='date_label'] li[role='option']"))
        )
        
        xpath = f"//ul[contains(@class, 'listbox') and @aria-labelledby='date_label']//li[@data-value='{data_value}']"
        day_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].click();", day_option)
        
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "button.js-date-button"), day_text)
        )
        current_text = driver.find_element(By.CSS_SELECTOR, "button.js-date-button").text.strip()
        print(f"Button text after click: '{current_text}' (expected: '{day_text}')")
        
        html = driver.page_source
        movies = parse_movies(html, base_site)
        movies_by_day[day_text] = movies
        print(f"Collected {len(movies)} movies for day: {day_text}")
    
    driver.quit()
    return movies_by_day
