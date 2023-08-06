
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.keys import Keys 
import time 





class login:
    def __init__(self,username,password,address):
        self.username=username
        self.password=password
        self.address=address
    def Facebook(self):
        browser = webdriver.Chrome(self.address) 
        
        browser.get('https://www.facebook.com/') 
        browser.maximize_window()
        element = browser.find_elements_by_xpath('//*[@id ="email"]') 
        element[0].send_keys(self.username) 
        element = browser.find_element_by_xpath('//*[@id ="pass"]') 
        element.send_keys(self.password) 
        log_in = browser.find_elements_by_id('loginbutton') 
        log_in[0].click() 

    def Instagram(self):
        browser = webdriver.Chrome(self.address) 
        browser.get('https://www.instagram.com/') 
        browser.maximize_window()
        element = browser.find_elements_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input') 
        element[0].send_keys(self.username) 
        element = browser.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input') 
        element.send_keys(self.password)  
        log_in = browser.find_elements_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]') 
        log_in[0].click() 

    def LinkedIn(self):
        browser = webdriver.Chrome(self.address) 
        browser.get('https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2F&fromSignIn=true&trk=cold_join_sign_in') 
        browser.maximize_window()
        element = browser.find_elements_by_xpath('//*[@id="username"]') 
        element[0].send_keys(self.username) 
        element = browser.find_element_by_xpath('//*[@id="password"]') 
        element.send_keys(self.password) 
        log_in = browser.find_elements_by_xpath('/html/body/div[1]/main/div[2]/form/div[3]/button') 
        log_in[0].click() 

    def Twitter(self):
        browser = webdriver.Chrome(self.address) 
        browser.get('https://www.twitter.com/') 
        browser.maximize_window()
        element = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div/main/div/div/div/div[1]/div[1]/div/form/div/div[1]/div/label/div/div[2]/div/input') 
        element[0].send_keys(self.username) 
        element = browser.find_element_by_xpath('/html/body/div[1]/div/div/div/main/div/div/div/div[1]/div[1]/div/form/div/div[2]/div/label/div/div[2]/div/input') 
        element.send_keys(self.password) 
        log_in = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div/main/div/div/div/div[1]/div[1]/div/form/div/div[3]/div/div/span/span') 
        log_in[0].click() 
     

    def Reddit(self):
        browser = webdriver.Chrome(self.address) 
        browser.get('https://www.reddit.com/login/') 
        browser.maximize_window()
        element = browser.find_elements_by_xpath('//*[@id="loginUsername"]') 
        element[0].send_keys(self.username) 
        element = browser.find_element_by_xpath('//*[@id="loginPassword"]') 
        element.send_keys(self.password) 
        log_in = browser.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/form/div[1]/fieldset[5]/button') 
        log_in[0].click() 



