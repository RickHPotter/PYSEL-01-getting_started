# Code With Tim - 6 Videos Playlist about Selenium on Python


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains

import time

driver = webdriver.Chrome('C:/Users/Rick H Potter/Desktop/Python/chromedriver')
driver.get("https://images.google.com/?gws_rd=ssl")

print(driver.title)

search_bar = driver.find_element_by_name("q")
search_bar.clear()
search_bar.send_keys("getting started with python")
search_bar.send_keys(Keys.RETURN)

print(driver.current_url)

driver.get("https://www.techwithtim.net/?s=test")

try:
	main = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.ID, "main"))
	)
	
	articles = main.find_elements_by_tag_name("article")
	for article in articles:
		header = article.find_element_by_class_name("entry-summary")
		print(header.text)

except:
	driver.quit()



driver.get("https://techwithtim.net")

time.sleep(3)

try:
	link = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.LINK_TEXT, "Python Programming"))
	)
	# link.clear()
	link.click()

	elementUn = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.LINK_TEXT, "Beginner Python Tutorials"))
	)
	# elementUn.clear()
	elementUn.click()

	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.ID, "sow-button-19310003"))
	)
	# element.clear()
	element.click()
	# driver.back()
	# driver.forward()
except:
	print("fucky")

# 2 - Cookie Clicker

try:
	driver.get("https://orteil.dashnet.org/cookieclicker/")
	driver.implicitly_wait(5)

	cookie = driver.find_element_by_id("bigCookie")
	cookie_count = driver.find_element_by_id("cookies")
	items = [driver.find_element_by_id("productPrice" + str(i)) for i in range(1, -1, -1)]

	actions = ActionChains(driver)
	actions.click(cookie)

	for i in range(70):
		actions.perform()
		count = cookie_count.text.split(" ")[0]
		for item in items:
			value = int(item.text)
			if value <= count:
				upgrade_actions = ActionChains(driver)
				upgrade_actions = ActionChains.move_to_element(item)
				upgrade_actions.click()
				upgrade_actions.perform()

except:
	print("fuck")

# driver.close()
