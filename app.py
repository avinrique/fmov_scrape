# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# #from webdriver_manager.chrome import ChromeDriverManager
# import json
# from time import sleep
# chrome_options = Options()
# chrome_options.add_argument("--headless=new")
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://fmovies.llc/home")
# driver.implicitly_wait(0.5)

# def get_input_search():
#     ins = input("enter movie name")
#     keyword_input = driver.find_element(By.NAME, "keyword")
#     keyword_input.send_keys(ins)
#     keyword_input.send_keys(Keys.RETURN)

# driver.implicitly_wait(5)
# flw_items = driver.find_elements(By.CLASS_NAME, "flw-item")

# movie_details = []


# for item in flw_items:
#     img_element = item.find_element(By.TAG_NAME, 'img')
#     img_src = img_element.get_attribute('src')
#     a_element = item.find_element(By.XPATH, './/h2[@class="film-name"]/a')
#     movie_link = a_element.get_attribute('href')
#     movie_name = a_element.get_attribute('title')


#     quality_element = item.find_element(By.CLASS_NAME, 'film-poster-quality')
#     quality = quality_element.text.strip()
#     fd_infor_element = item.find_element(By.CLASS_NAME, 'fd-infor')
#     fdi_items = fd_infor_element.find_elements(By.CLASS_NAME, 'fdi-item')
#     season = None
#     episode = None
#     for fdi_item in fdi_items:
#         item_text = fdi_item.text.strip()
#         if "SS" in item_text:
#             season = item_text
#         elif "EPS" in item_text: 
#             episode = item_text
   
#     movie_type = fdi_items[-1].text.strip()  
#     movie_details.append({
#         'Image Source': img_src,
#         'Movie Link': movie_link,
#         'Quality': quality,
#         'Movie Type': movie_type,
#         'Duration': None, 
#         'Movie Name': movie_name,
#         'Season': season,
#         'Episode': episode
#     })
#     with open('movie_data.json', 'w') as f:
#         json.dump(movie_details, f, indent=4)


# nextpage = driver.find_elements(By.CLASS_NAME,"page-item")

# for pages in nextpage :
#     aofpages = pages.find_element(By.TAG_NAME,"a")
#     if aofpages.get_attribute("title") ==  "Next" :
#         print(aofpages.get_attribute("href"))

# # nextpage = nextpage.find_element(By.)
# for movie in movie_details:
#     print(movie)
# driver.quit()

# #<input type="text" autocomplete="off" name="keyword" placeholder="Enter keywords..." class="form-control search-input">

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys

def scrape_movies(search_query):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://fmovies.llc/home")
    ins = search_query
    keyword_input = driver.find_element(By.NAME, "keyword")
    keyword_input.send_keys(ins)
    keyword_input.send_keys(Keys.RETURN)
    driver.implicitly_wait(1)
    movies = []
    wait = WebDriverWait(driver, 10)
    flw_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flw-item")))

    for item in flw_items:
        img_element = item.find_element(By.TAG_NAME, 'img')
        img_src = img_element.get_attribute('src')
        a_element = item.find_element(By.XPATH, './/h2[@class="film-name"]/a')
        movie_link = a_element.get_attribute('href')
        movie_name = a_element.get_attribute('title')

        quality_element = item.find_element(By.CLASS_NAME, 'film-poster-quality')
        quality = quality_element.text.strip() if quality_element else 'Unknown'

        fd_infor_element = item.find_element(By.CLASS_NAME, 'fd-infor')
        fdi_items = fd_infor_element.find_elements(By.CLASS_NAME, 'fdi-item')
        season = None
        episode = None

        for fdi_item in fdi_items:
            item_text = fdi_item.text.strip()
            if "SS" in item_text:
                season = item_text
            elif "EPS" in item_text:
                episode = item_text
        
        movie_type = fdi_items[-1].text.strip() if fdi_items else 'Unknown'
        
        movies.append({
            'Image Source': img_src,
            'Movie Link': movie_link,
            'Quality': quality,
            'Movie Type': movie_type,
            'Movie Name': movie_name,
            'Season': season,
            'Episode': episode
        })

    driver.quit()
    return movies

if __name__ == "__main__":
    search_query = sys.argv[1] if len(sys.argv) > 1 else "the place"
    movies = scrape_movies(search_query)
    print(json.dumps(movies))











