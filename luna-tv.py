import requests
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

source_url = 'https://www.fready.co/stats_data'
sound_loc = "success.mp3"
print('Starting out with ' + str(json.loads(requests.get(source_url).content)['users']) + ' users!')



browser = webdriver.Firefox()

browser.get('https://www.facebook.com/messages/t/3325816220790219')
action = ActionChains(browser)


elem = browser.find_element_by_id('email')
elem.send_keys('lukethebaker420@gmail.com')
elem = browser.find_element_by_id('pass')
elem.send_keys('lukebakerhasbigpeepee' + Keys.RETURN)

time.sleep(3)

# elem = browser.find_element_by_class_name('navigationFocus')
# elem.send_keys('yo im here and you guys have some shit' + Keys.RETURN)
# create action chain object
# browser.quit()
def send_msg(content):
    action = ActionChains(browser)
    action.send_keys(content + Keys.ENTER).perform()

def load_data():
  return json.loads(requests.get(source_url).content)

def load_users():
  return int(load_data()['users'])

last_user_count = 0
while True:
  user_count = load_users()
  if user_count>last_user_count:
    send_msg('New user 🥳! Total users: ' + str(user_count) )

    last_user_count = user_count
    os.system("afplay " + sound_loc)
    print('>>> ' + str(last_user_count) + ' users!')
    os.system("say a new wild user has appeared." + "Now Fready has " + str(last_user_count) + " users")

  time.sleep(10)
