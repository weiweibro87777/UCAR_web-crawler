import requests
from bs4 import BeautifulSoup
import pandas as pd


#程式歡迎語
print("**歡迎來到UCAR爬蟲程式**")
print("\n")

#將資料存入建立好的list
titles = []
date = []
url_list = []
clicks =[]
replys = []

#自定義查詢關鍵字及日期區間
x = str(input("請輸入想爬取的關鍵字："))
print("日期格式輸入範例(YYYYMMDD)：20200715")
print("\n")
start_date = int(input("請輸入想爬取的起始日期："))		#格式YYYYMMDD:20180101
end_date = int(input("請輸入想爬取的結束日期："))		#格式YYYYMMDD:20191231
fake_request_url= "https://forum.u-car.com.tw/forum/list?keywords=" + x

print("\n")
print("爬取中...請稍後")

#抓使用者輸入之關鍵字所有網頁
z = 0
while(True):
	z += 1
	real_request_url = fake_request_url + "&page=" + str(z)
	#print(real_request_url)
	response = requests.get(real_request_url)
	response_text = response.text
	soup = BeautifulSoup(response_text, "html.parser")
	#print(soup)

#判斷這一頁目錄有沒有文章(有就接下一步，沒有就break)
#值得注意的是，這裡查詢每個目錄頁是否存在.writer而不是用.title的原因為，在該目錄頁沒有文章是還是有存在.title標籤，所以選擇.writer為判斷依據
	if soup.select(".writer"):
		pass
	else:
		break

#將所有div class="cell_topic"的內容爬下來儲存到變數soup.find1(是個list)
	soup_find1 = soup.find_all('div', 'cell_topic')
#抓發文日期
	#迴圈soup_find1這個list
	for i in range(len(soup_find1)):
		#第一頁且list前兩項0,1是置頂廣告，所以continue
		if (z == 1 and i <= 1):
			continue
		b = soup_find1[i].find('div', 'postby margin-right-10').find('p').text
		#print(b)
		re_b = b[:10]
		#print(re_b)
		re_b_b = int(re_b.replace('/', ''))
		#print(re_b_b)
		#print(re_b)

#判斷發文日期是否符合使用者需求並丟到list
		if (start_date <= re_b_b and re_b_b <= end_date):
			pass
		else:
			continue
		date.append(re_b)
		#print(re_b)

#抓網址
		url = soup_find1[i].find('div', 'title').find('a')
		#print(url)
		a = 'https://forum.u-car.com.tw'
		if url is not None:
			url_list.append(a + url.get('href'))
		else:
			url_list.append("(本文已被刪除)")
		#print(a + url.get('href'))

#抓標題
		c = soup_find1[i].find('div', 'title').find('a')
		#print(c)
		if c is not None:
			titles.append(c.text)
		else:
			titles.append('(本文已被刪除)')
		print(c.text)

#抓點閱數
		click_count = soup_find1[i].find('div', 'cell_topic_view').find('p')
		if click_count is not None:
			clicks.append(click_count.text)
		else:
			clicks.append("0")
		#print(click_count.text)

#抓回覆數
		replys_count = soup_find1[i].find('div', 'cell_topic_chats').find('p')
		if click_count is not None:
			replys.append(replys_count.text)
		else:
			replys.append("0")
		#print(replys_count.text)
	#print('46行迴圈結束')

print("\n")
print("轉檔中...請稍後")

#轉為DataFrame
df = pd.DataFrame(
    {
        '標題' : titles,
		'點閱數' : clicks,
		'回覆數' : replys,
        '發文日期' : date,
        '文章連結' : url_list
    }
)

#另存為csv
df.to_csv( "UCAR_" + x +"回傳結果.csv", index = False, encoding = "utf_8_sig")

#程式結束
len_titles = len(titles)
print("本次共爬出 {} 篇文章".format(len_titles))
print("\n")
end = input("請輸入任意鍵結束程式：")
