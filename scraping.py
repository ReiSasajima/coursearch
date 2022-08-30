# from turtle import back
# import idna
from distutils.spawn import find_executable
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os, signal
import csv
import datetime
from pyshorteners import Shortener


# 出力するCSVのファイル名に日付を付与
csv_date = datetime.datetime.today().strftime("%Y%m%d")
csv_file_name = 'agusyllabus_' + csv_date + '.csv'
# 空のCSVファイルに書き込み
f = open(csv_file_name, 'w', encoding='cp932', errors='ignore')

writer = csv.writer(f, lineterminator='\n') 
# csv_header = ["授業時間","授業名","講師名","教室番号","授業評価方法"]
csv_header = ["授業時間","授業名","講師名","授業評価方法","URL"]
writer.writerow(csv_header)

# 短縮URLモジュール
s = Shortener()
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
# driver.get('https://aguinfo.jm.aoyama.ac.jp/kouginaiyou/kensaku.aspx')
# driver.get('https://aguinfo.jm.aoyama.ac.jp/kouginaiyou/kensaku.aspx?__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATEGENERATOR=4B2C0FF9&BU=BU1&KW=&KM=&KI=&CP1=on&GB1B_0=&GKB=&DL=ja&ctl00%24CPH1%24btnKensaku=%E6%A4%9C%E7%B4%A2%2FSearch&ST=&PG=&PC=&PI=')

# driver.get('https://aoyama-portal.aoyama.ac.jp/aogaku_auth/jsp/AUTH01.jsp?TYPE=33554433&REALMOID=06-2a27689c-587a-42e0-834c-7a6751c24219&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-y%2fO%2bwXHmQFuKEoGlz9CdfIzo1Ujfp%2fcsgj66pcDn%2bqoJ8OCObeoRcIMe463sPxZH&TARGET=-SM-https%3a%2f%2faoyama--portal%2eaoyama%2eac%2ejp%2fprotect%2f')

# id = driver.find_element_by_xpath("/html/body/div/table/tbody/tr/td/table/tbody/tr[1]/td[1]/form/table/tbody/tr[2]/td[2]/input")
# id.send_keys("a3119233")
# password = driver.find_element_by_xpath("/html/body/div/table/tbody/tr/td/table/tbody/tr[1]/td[1]/form/table/tbody/tr[3]/td[2]/input")
# password.send_keys("ssjm01194AU")
# login = driver.find_element_by_xpath("/html/body/div/table/tbody/tr/td/table/tbody/tr[1]/td[1]/form/table/tbody/tr[4]/td[2]/input")
# login.click()
# syllabus = driver.find_element_by_xpath("/html/body/form/div[3]/div[1]/div[2]/ul[8]/li[7]/a")
# syllabus.click()

# 大学キャンパスの選択
# (青山を選択)

campus = driver.find_element_by_id('CPH1_rptCP_CP_0')
campus.click()
# (相模原を選択)
# campus = driver.find_element_by_id('CPH1_rptCP_CP_1')
# campus.click()

# 検索ボタン
search = driver.find_element_by_id('CPH1_btnKensaku')
search.click()

for j in range(0, 5):
  for i in range(0, 20):
    dateTime = driver.find_element_by_id(f'CPH1_gvw_kensaku_lblJigen_{i}')
    title = driver.find_element_by_id(f'CPH1_gvw_kensaku_lblKamoku_{i}')
    lecturerName = driver.find_element_by_id(f'CPH1_gvw_kensaku_lblKyouin_{i}')
    # room = driver.find_element_by_id(f'CPH1_gvw_kensaku_lblRoom_{i}')
    
    csvlist = []
    csvlist.append(dateTime.text)
    csvlist.append(title.text)
    csvlist.append(lecturerName.text)
    # csvlist.append(room.text)

    print(dateTime.text, '授業名:', title.text, '講師名:', lecturerName.text)
    # 詳細ページ
    detail = driver.find_element_by_id(f'CPH1_gvw_kensaku_lnkShousai_{i}')
    driver.execute_script('arguments[0].click();', detail)
    # URLの取得
    cur_url = driver.current_url
    # URLの短縮実行
    shortened_link = s.tinyurl.short(cur_url)
    # 短縮URLをCSVに追加
    csvlist.append(shortened_link)
    print(shortened_link)
    # if driver.find_element_by_id('CPH1_gvSeiseki'):
    #   evaluation = driver.find_element_by_id('CPH1_tr_Seiseki')
    try:
      evaluation = driver.find_element_by_id('CPH1_gvSeiseki')
      print(evaluation.text)
      csvlist.append(evaluation.text)
    except NoSuchElementException:
      print('データなし')
      csvlist.append('データなし')
    writer.writerow(csvlist)
    print()
    # 戻るボタン
    backBtn = driver.find_element_by_id('hypBack')
    backBtn.click()
  
  # 次のページへのボタン
  driver.implicitly_wait(10)
  nextBtn = driver.find_element_by_id('CPH1_rptPagerB_lnkNext')
  driver.execute_script('arguments[0].click();', nextBtn)

f.close()
# try:
#   nextBtn1 = driver.find_element_by_id('CPH1_rptPagerB_lnkNext')
#   nextBtn1.click()
# except NoSuchElementException:
#   None

# chromeを開いたままpython seleniumを終了してchromeを開いたままにする
os.kill(driver.service.process.pid, signal.SIGTERM)


