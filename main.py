import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window()

url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

#check 모두 해제
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected():
        checkbox.click()

items_to_select = ['영업이익', '자산총계', '매출액']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') #find parent element
    label = parent.find_element(By.TAG_NAME, 'label')
    #print(label.text)
    if label.text in items_to_select:
        checkbox.click()
    
#4. apply
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]') #find <a> tag which has "href" propery and propery value is "javascript:fieldSubmit()"
btn_apply.click()

for idx in range(1, 40):
    # page move
    browser.get(url + str(idx))
    
    #5. get data
    df = pd.read_html(browser.page_source)[1]
    df.dropna(axis='index', how='all', inplace=True) #해당 row가 모두 NaN면 제거
    df.dropna(axis='columns', how='all', inplace=True) #해당 col이 모두 NaN면 제거
    if len(df) == 0:
        break;

    #6. file save
    f_name = 'saved_stock.csv'
    if os.path.exists(f_name): #file existed?, do not make header
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else: #no file? make header also.
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=True)

    print(f'{idx} page done')

browser.quit()
