import requests
import json

#password qb9XrT53n!Rm:@^

def cookieGen():
    # If there is no auth cookie present, this will login via Selenium and create the nec cookie file
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
    from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    
    # Collect necessary login and password information from the user
    print("Authentication cookies not found. Please provide login and password to generate authentication cookies.")
    espnLogin = str(input("Login: "))
    espnPw = str(input("Password: "))
    
    # Login to ESPN with Selenium
    driver = webdriver.Chrome()
    driver.get('https://fantasy.espn.com/baseball/team?leagueId=97325&teamId=8&seasonId=2022')
    WebDriverWait(driver, 1000).until(EC.presence_of_all_elements_located((By.XPATH, "(//iframe)")))
    frms = driver.find_elements("xpath", '(//iframe)')
    driver.switch_to.frame(frms[0])
    time.sleep(3)
    driver.find_element("xpath", '(//input)[1]').send_keys(espnLogin)
    driver.find_element("xpath", '(//input)[2]').send_keys(espnPw)
    driver.find_element("xpath", '//button').click()
    driver.switch_to.default_content()
    time.sleep(36)

    # Pull, reformat, and write the cookie information to a .json file
    cookies = {}
    seleniumCookies = driver.get_cookies()
    
    for cookie in seleniumCookies:
        cookies[cookie['name']] = cookie['value']
    
    json.dump(cookies, open("cookies.json","w"))
    
    return

league_id = 97325
year = 2023
url = "https://fantasy.espn.com/apis/v3/games/flb/seasons/" + \
     str(year) + "/segments/0/leagues/" + str(league_id) 

session = requests.Session()


while True:
    try:
        with open('cookies.json', 'r') as f:
            print("***************")
            print()
            print("***************")
            session.cookies.update(json.load(f))
        break
    except FileNotFoundError:
        cookieGen()



#r = session.get(url)

#r = session.post(url+"/transactions/", json={"isLeagueManager":False,"teamId":8,"type":"ROSTER","memberId":"{577ECCF9-EF3F-4F3E-A9F5-6CAC18427C9D}","executionType":"EXECUTE","items":[{"playerId":5986,"type":"LINEUP","fromLineupSlotId":12,"toLineupSlotId":0}]})
r = session.get("https://fantasy.espn.com/apis/v3/games/flb/seasons/2023/segments/0/leagues/97325?rosterForTeamId=8")
#d = r.json()

print(r.text)