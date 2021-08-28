import requests
import csv
from csv import reader
from bs4 import BeautifulSoup

# 目標URL網址
URL = "https://forum.gamer.com.tw/B.php?page=1&bsn=60508"

def get_resource(url):
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
    return requests.get(url, headers=headers) 

def parse_html(r):
    if r.status_code == requests.codes.ok:
        r.encoding = "utf8"
        soup = BeautifulSoup(r.text, "html.parser")
        print("連線成功...")
    else:
        print("HTTP請求錯誤..." + URL)
        soup = None
    return soup

def web_scraping_bot(url):
    print("抓取網路資料中...")
    soup = parse_html(get_resource(url))
    if soup != None:
      tag = soup.find_all('tr',class_='b-list__row b-list-item b-imglist-item')
      pvc_inf = []
      for i in range(len(tag)):
          # title = tag[i].find('p',class_='b-list__main__title').text
          # context = tag[i].find('p',class_='b-list__brief').text
          pvc_url = 'https://forum.gamer.com.tw/'+str(tag[i].select('a')[2].get('href'))
          # po_time = tag[i].find('p',class_='b-list__time__edittime').text.replace('\n','')
          
          if 'pvc' in tag[i].find('p',class_='b-list__main__title').text:
              pvc_inf.append(pvc_url)
          elif 'PVC' in tag[i].find('p',class_='b-list__main__title').text:
              pvc_inf.append(pvc_url)
          elif '吉普莉爾' in tag[i].find('p',class_='b-list__main__title').text:
              pvc_inf.append(['吉普莉爾',pvc_url])
          elif '黏土人' in tag[i].find('p',class_='b-list__main__title').text:
              pvc_inf.append(pvc_url)
          else:
              continue
    else:
      return 'ERROR'
    pvc_inf, pvc_inf_old = compare_list(pvc_inf)
    save_to_csv(pvc_inf_old, 'file.csv')
    return pvc_inf

def save_to_csv(pvc_inf, file):
    with open(file, 'w+', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(pvc_inf)

def compare_list(pvc_inf_new):
    pvc_inf = []
    with open('file.csv', 'r') as csv_file:
        csv_reader = reader(csv_file)
        pvc_inf_old = list(csv_reader)
        for i in pvc_inf_new:
            try:
                if i not in pvc_inf_old[0]:
                    pvc_inf.append(i)
                    pvc_inf_old[0].append(i)
            except:
                return pvc_inf_new,pvc_inf
    return pvc_inf,pvc_inf_old[0]

def clear_file():
    with open('file.csv', 'r') as csv_file:
        csv_reader = reader(csv_file)
        csv_reader = []
        save_to_csv(csv_reader, 'file.csv')

def runpvc():
    pvc_inf = web_scraping_bot(URL)
    return pvc_inf