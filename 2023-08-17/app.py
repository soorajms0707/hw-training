# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# import time

# driver = webdriver.Chrome()
# driver.get("http://www.google.com")
# time.sleep(5)

# driver.close()



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://www.google.com/")
time.sleep(2)
searchbox=driver.find_element(By.CLASS_NAME,"gLFyf")
searchbox.send_keys("ronaldo")
searchbox.send_keys(Keys.RETURN)
time.sleep(4)
driver.close()


driver = webdriver.Chrome()
driver.get("https://en.wikipedia.org/wiki/Cristiano_Ronaldo")
time.sleep(2)
titlename=driver.find_element(By.CLASS_NAME,"mw-page-title-main")

print(titlename.text+"this is the name")
# searchbox.send_keys(Keys.RETURN)
time.sleep(4)
driver.close()




# driver.get("https://codebeautify.org/random-quote-generator")
# time.sleep(2)
# lis=[]
# for i in range(10):
#     inpt_num=driver.find_element(By.ID,"inputRandomNumber")
#     inpt_num.send_keys("1")
#     time.sleep(4)
#     button=driver.find_element(By.CLASS_NAME,"control")
#     button.click()
#     time.sleep(4)
#     qoute=driver.find_element(By.CLASS_NAME,"Quotes")
#     lis.append(qoute.text)

# print(lis)

# # searchbox.send_keys(Keys.RETURN)
# time.sleep(4)
# driver.close()