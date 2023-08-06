This module will help you to login in all social networking accounts like facebook ,instagram ,linkedin ,reddit and twitter from your python IDE without reaching to the sites .

It will automaticlly login your social accounts in a separate chrome driver window .



How does it work ?

Step I -You have to install this package login-all, selenium package and chrome webdriver.

Step II-Then type -> from easy_login import login in your script.

Step III-obj=login(username ,password ,address_of_chrome_webdriver)

Step IV -Start Loging in  your accounts .

obj.facebook()
obj.instagram()
obj.twitter()
obj.reddit()
obj.linkedin()

Step V- Done . 




Note:
1-Uername and password must be of same account which you have to Login .

2-Address must be in format - C:/Users/Vasu Gupta/chromedriver_win32/chromedriver

