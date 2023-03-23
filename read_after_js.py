# Copyright (C) 2023 Warren Usui, MIT License
"""
Get page text after javascript is run
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_text_after_js_processing(in_text):
    """
    Use selenium driver to get post javascript output.  In_text is the
    webpage being checked.  The contents of the page are returned.
    """
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=options)
    driver.get(in_text)
    return driver.page_source

if __name__ == "__main__":
    TXT = 'https://fantasy.espn.com/tournament-challenge-bracket/2023/en/'
    TXT += 'group?groupID=5157379'
    print(get_text_after_js_processing(TXT))
