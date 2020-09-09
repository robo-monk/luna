import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import click
from datetime import datetime
fready_url = 'http://localhost:3000'

# helpers
def to(url):
  driver.get(fready_url + url)
  
def go_home():
  driver.get(fready_url);

def scan(string):
  return driver.find_elements_by_xpath("//*[contains(text(),'" + string + "')]")
def bclick(string):
  scan(string)[0].click()

def sign_in(user):
  if signed_in_(test_user['name']):
    go_home()
  else:
    time.sleep(.3)
    action = ActionChains(driver)
    action.send_keys(user['email'] + Keys.TAB + "123456789" + Keys.ENTER).perform()
  
  
def sign_out():
  if (signed_in_(test_user['name']) or signed_in_('Luna 2')):
    go_home()
    time.sleep(.4)
    to('/myprofile')
    time.sleep(.6)
    bclick('Log Out')
  
def pretty_print_tests(tests):
  for key, value in tests.items():
    if value:
      click.secho(key + " : " + 'PASS', fg='green')
    else:
      click.secho(key + " : " + 'FAIL', fg='red') 
      
def screen(filename):
  driver.get_screenshot_as_file(test_folder + "/" + filename + ".png")

def keyz(string):
  action = ActionChains(driver)
  action.send_keys(string).perform()

def fill_sign_up(name, email):
  action = ActionChains(driver)
  action.send_keys(name + Keys.TAB + email + Keys.TAB + "123456789" + Keys.TAB + "123456789" + Keys.ENTER).perform()

def signed_in_(name):
  to('/myprofile')
  time.sleep(.2)
  return len(scan(name)) > 0
 
 
# trip tests

def test_sign_out():
  if (signed_in_(test_user['name'])):
    go_home()
    time.sleep(.7)
    to('/myprofile')
    time.sleep(.6)
    bclick('Log Out')
    time.sleep(.5)
    
  return len(scan('Spend less time reading.')) > 0

def test_log_in():
  if (signed_in_(test_user['name'])):
    go_home()
    sign_out()
    
  go_home()
  bclick('Log In')
  sign_in(test_user)
  time.sleep(.5)
    
  return signed_in_(test_user['name'])
  
def test_profile():
  go_home()
  time.sleep(.4)
  to('/myprofile')
  time.sleep(.6)
  screen('profile')
  return len(scan(test_user['name'])) > 0
 
def test_sign_ups():
  go_home()
  bclick('Sign Up')
  time.sleep(1)
  # action = ActionChains(driver)
  # action.send_keys(test_user['name'] + Keys.TAB + test_user['email'] + Keys.TAB + "123456789" + Keys.TAB + "123456789" + Keys.ENTER).perform()
  fill_sign_up(test_user['name'], test_user['email'])
  time.sleep(1)
  screen('aftersignup')
  time.sleep(1)

  return signed_in_(test_user['name'])

def test_welcome_sign_up():
  sign_out()
  time.sleep(.3)
  to('/welcome')
  screen('welcome')
  time.sleep(.3)
  fill_sign_up('Luna 2', 'luna-xfready@gmail.com')
  screen('first screen after welcome sign up')
  time.sleep(.3)
  return signed_in_('Luna 2')
 
def test_archive():
  sign_in(test_user)
  go_home()
  driver.find_elements_by_xpath("//a[@href='/archive']")[0].click()
  time.sleep(.5)
  screen('archieve')
  return len(scan('Archive')) > 0

def test_splash():
  go_home()
  sign_out()
  go_home()
  time.sleep(.1)
  screen('splash')
  return len(scan('Spend less time reading.')) > 0

def test_early_access():
  sign_in(test_user)
  go_home()
  bclick('Books')
  screen('Early Access page')
  return len(scan(' Stay focused when reading your books. ')) > 1

def test_read_article():
  sign_in(test_user)
  go_home()
  bclick('Articles')
  driver.find_elements_by_class_name("link_blokkkk")[0].click()
  time.sleep(1)
  screen('lector-1')
  time.sleep(1)
  screen('lector-2')
  keyz(' ')
  time.sleep(3)
  screen('lector-3')
  time.sleep(4)
  return len(scan('speed'))   

 
def run_tests():
  tests = {
    'normal sign up': test_sign_ups(),
    'profile': test_profile(),
    'sign out': test_sign_out(),
    'log in': test_log_in(),
    'sign up from xfready': test_welcome_sign_up(),
    'archive': test_archive(),
    'splash': test_splash(),
    'early access': test_early_access(),
    'read article': test_read_article()
  }
  print(" ") 
  click.secho(' - TEST RESULTS - ', bg='blue')
  print(" ")
  pretty_print_tests(tests)



# initiate program
test_user = { 
   'name': 'Luna Paparouna',
   'email': 'lunatestuser1@gmail.com'
  }

print('Starting up the test...')
print("""Please run in rails console: \n
      u = User.find_by_email('lunatestuser1@gmail.com'); u.delete();u = User.find_by_email('luna-xfready@gmail.com'); u.delete()
      """)
print("""

 ___       ___  ___  ________   ________     
|\  \     |\  \|\  \|\   ___  \|\   __  \            
\ \  \    \ \  \\\  \ \  \\ \  \ \  \|\  \            
 \ \  \    \ \  \\\  \ \  \\ \  \ \   __  \            
  \ \  \____\ \  \\\  \ \  \\ \  \ \  \ \  \           
   \ \_______\ \_______\ \__\\ \__\ \__\ \__\            
    \|_______|\|_______|\|__| \|__|\|__|\|__|
 
""")
print("        TESTING:  " + fready_url) 
          
driver = webdriver.Chrome('chromedriver')  # Optional argument, if not specified will search path.
driver.get(fready_url);

test_folder = "tests/t-" + str(datetime.now())

if input('Launch? ') == 'y':
  os.mkdir(test_folder)
  run_tests()

print('--end of test')
driver.quit()