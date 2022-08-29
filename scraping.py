# from turtle import back
# import idna
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os, signal
import csv

# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)

# 下のoption addargumentでブラウザ非表示で実行
# options = Options()
# options.add_argument('--headless')
# chromeoption=optionsでブラウザ非表示を適用
# driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)
# driver.get('https://aoyama-portal.aoyama.ac.jp/aogaku_auth/jsp/AUTH01.jsp?TYPE=33554433&REALMOID=06-2a27689c-587a-42e0-834c-7a6751c24219&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-y%2fO%2bwXHmQFuKEoGlz9CdfIzo1Ujfp%2fcsgj66pcDn%2bqoJ8OCObeoRcIMe463sPxZH&TARGET=-SM-https%3a%2f%2faoyama--portal%2eaoyama%2eac%2ejp%2fprotect%2f')

driver.get('http://syllabus.aoyama.ac.jp/')
# driver.get('https://aoyama-portal.aoyama.ac.jp/aogaku_auth/jsp/AUTH01.jsp?TYPE=33554433&REALMOID=06-2a27689c-587a-42e0-834c-7a6751c24219&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-y%2fO%2bwXHmQFuKEoGlz9CdfIzo1Ujfp%2fcsgj66pcDn%2bqoJ8OCObeoRcIMe463sPxZH&TARGET=-SM-https%3a%2f%2faoyama--portal%2eaoyama%2eac%2ejp%2fprotect%2f')

# 授業名の項目
# courseTitle = driver.find_element_by_id('CPH1_KM')
# courseTitle.send_keys("")

# 大学キャンパスの選択(下は青山を選択)
campus = driver.find_element_by_id('CPH1_rptCP_CP_0')
campus.click()

# 検索ボタン
search = driver.find_element_by_id('CPH1_btnKensaku')
search.click()


for i in range(0, 20):
  dateTime = driver.find_element_by_id(f'CPH1_gvw_kensaku_lblJigen_{i}')
  title = driver.find_element_by_id(f'CPH1_gvw_kensaku_lblKamoku_{i}')
  lecturerName = driver.find_element_by_id(f'CPH1_gvw_kensaku_lblKyouin_{i}')
  print(dateTime.text, '授業名:', title.text, '講師名:', lecturerName.text)
  # 詳細ページ
  detail = driver.find_element_by_id(f'CPH1_gvw_kensaku_lnkShousai_{i}')
  driver.execute_script('arguments[0].click();', detail)
  # detail.click()
  # if driver.find_element_by_id('CPH1_gvSeiseki'):
  #   evaluation = driver.find_element_by_id('CPH1_tr_Seiseki')
  try:
    evaluation = driver.find_element_by_id('CPH1_gvSeiseki')
    print(evaluation.text)
  except NoSuchElementException:
    print('データなし')

  print()
  # 戻るボタン
  backBtn = driver.find_element_by_id('hypBack')
  backBtn.click()

# 次のページへのボタン
nextBtn1 = driver.find_element_by_id('CPH1_rptPagerB_lnkPage_1')
nextBtn1.click()

# chromeを開いたままpython seleniumを終了してchromeを開いたままにする
os.kill(driver.service.process.pid, signal.SIGTERM)


