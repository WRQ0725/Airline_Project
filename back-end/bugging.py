from lxml import etree
import requests
import random
import time
import csv
import pandas as pd 
import numpy as np

cookies = {
    '_RDG': '289fda7de3273426211d373ea0161b1ef2',
    '_RGUID': 'f09ac836-d3f1-4c04-8d4b-de170ffcd0d5',
    '_RSG': '4mKyJR3oQ2FL3D_FSXtBr8',
    'MKT_CKID': '1622443083256.9m8qg.vewg',
    '_ga': 'GA1.2.707014534.1622443083',
    'GUID': '09031042214511715343',
    'nfes_isSupportWebP': '1',
    '_bfaStatusPVSend': '1',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2217fb6f458bde18-07dae8d00d6fe-9771a3f-1296000-17fb6f458be72d%22%2C%22%24device_id%22%3A%2217fb6f458bde18-07dae8d00d6fe-9771a3f-1296000-17fb6f458be72d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fapp.mokahr.com%2F%22%2C%22%24latest_referrer_host%22%3A%22app.mokahr.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D',
    '__zpspc': '9.25.1657444518.1657444870.4%233%7Ccn.bing.com%7C%7C%7C%7C%23',
    'Session': 'SmartLinkCode=51cto&SmartLinkKeyWord=&SmartLinkQuary=_UTF.&SmartLinkHost=blog.51cto.com&SmartLinkLanguage=zh',
    '_RF1': '139.226.176.169',
    '_bfa': '1.1622443080329.1gik74.1.1709048025895.1709048029542.34.2.101021',
    '_ubtstatus': '%7B%22vid%22%3A%221622443080329.1gik74%22%2C%22sid%22%3A34%2C%22pvid%22%3A2%2C%22pid%22%3A101021%7D',
    '_bfaStatus': 'success',
    '_jzqco': '%7C%7C%7C%7C1710593260804%7C1.624638678.1708529546739.1709135182955.1710593260691.1709135182955.1710593260691.0.0.0.22.22',
}

headers = {
    'authority': 'flights.ctrip.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': '_RDG=289fda7de3273426211d373ea0161b1ef2; _RGUID=f09ac836-d3f1-4c04-8d4b-de170ffcd0d5; _RSG=4mKyJR3oQ2FL3D_FSXtBr8; MKT_CKID=1622443083256.9m8qg.vewg; _ga=GA1.2.707014534.1622443083; GUID=09031042214511715343; nfes_isSupportWebP=1; _bfaStatusPVSend=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217fb6f458bde18-07dae8d00d6fe-9771a3f-1296000-17fb6f458be72d%22%2C%22%24device_id%22%3A%2217fb6f458bde18-07dae8d00d6fe-9771a3f-1296000-17fb6f458be72d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fapp.mokahr.com%2F%22%2C%22%24latest_referrer_host%22%3A%22app.mokahr.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; __zpspc=9.25.1657444518.1657444870.4%233%7Ccn.bing.com%7C%7C%7C%7C%23; Session=SmartLinkCode=51cto&SmartLinkKeyWord=&SmartLinkQuary=_UTF.&SmartLinkHost=blog.51cto.com&SmartLinkLanguage=zh; _RF1=139.226.176.169; _bfa=1.1622443080329.1gik74.1.1709048025895.1709048029542.34.2.101021; _ubtstatus=%7B%22vid%22%3A%221622443080329.1gik74%22%2C%22sid%22%3A34%2C%22pvid%22%3A2%2C%22pid%22%3A101021%7D; _bfaStatus=success; _jzqco=%7C%7C%7C%7C1710593260804%7C1.624638678.1708529546739.1709135182955.1710593260691.1709135182955.1710593260691.0.0.0.22.22',
    'referer': 'https://flights.ctrip.com/schedule/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

def get_province_capitals():
    # 中国各省会城市（包括直辖市）列表
    return [
        "北京", "天津", "上海", "重庆",
        "石家庄", "太原", "呼和浩特", "沈阳",
        "长春", "哈尔滨", "南京", "杭州",
        "合肥", "福州", "南昌", "济南",
        "郑州", "武汉", "长沙", "广州",
        "南宁", "海口", "成都", "贵阳",
        "昆明", "拉萨", "西安", "兰州",
        "西宁", "银川", "乌鲁木齐", "台北",
        "香港", "澳门"
    ]


def flight_departure():
    # 首页网址URL
    url = 'https://flights.ctrip.com/schedule'
    # 请求发送
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    cookies = {}  # 如果需要，可以在这里添加cookies
    page_text = requests.get(url=url, cookies=cookies, headers=headers).text
    # 数据解析
    tree = etree.HTML(page_text)
    # 出发航班名称和链接
    flight_name = tree.xpath("//div[@class='m']/a/text()")
    flight_link = tree.xpath("//div[@class='m']/a/@href")
    
    # 获取省会城市列表
    province_capitals = get_province_capitals()
    
    # 筛选省会城市（包括直辖市）的航班信息
    filtered_flight_name = []
    filtered_flight_link = []
    for name, link in zip(flight_name, flight_link):
        if any(capital in name for capital in province_capitals):
            filtered_flight_name.append(name)
            filtered_flight_link.append(link)
    
    print("共获取到", len(filtered_flight_name), "条省会城市（包括直辖市）的航班信息！！")
    print(filtered_flight_name)
    return filtered_flight_name, filtered_flight_link

# 二级页面，获取机场之间存在往返航班记录的机场数，以及所有航班记录的三级链接
def flight_dep_arr(flight_name,flight_link):
    flight_name_2 = {} # 存储出发-到达的记录
    flight_link_2 = [] # 存储出发-到达的航班明细网页的链接
    for i in range(len(flight_name)): 
        time.sleep(1)
        url = 'https://flights.ctrip.com' + flight_link[i]
        page_text = requests.get(url=url, headers=headers).text
        tree = etree.HTML(page_text)

        name = tree.xpath("//div[@class='m']/a/text()")
        link = tree.xpath("//div[@class='m']/a/@href")
        
        print(flight_name[i],'数据已获取完，共和',len(name),'个机场有往返记录')
        name_dict = {flight_name[i]:name}
        flight_name_2.update(name_dict) # 字典合并
        flight_link_2.extend(link) # 数组合并
    return flight_name_2,flight_link_2

# 一对起始点的往返航班记录
def flight_dep_arr_detail(flight_link_2):
    cookies = {
        '_RSG': '4mKyJR3oQ2FL3D_FSXtBr8',
        '_RDG': '289fda7de3273426211d373ea0161b1ef2',
        '_RGUID': 'f09ac836-d3f1-4c04-8d4b-de170ffcd0d5',
        'MKT_CKID': '1622443083256.9m8qg.vewg',
        '_ga': 'GA1.2.707014534.1622443083',
        'GUID': '09031042214511715343',
        'nfes_isSupportWebP': '1',
        '_bfaStatusPVSend': '1',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2217fb6f458bde18-07dae8d00d6fe-9771a3f-1296000-17fb6f458be72d%22%2C%22%24device_id%22%3A%2217fb6f458bde18-07dae8d00d6fe-9771a3f-1296000-17fb6f458be72d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fapp.mokahr.com%2F%22%2C%22%24latest_referrer_host%22%3A%22app.mokahr.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D',
        '__zpspc': '9.25.1657444518.1657444870.4%233%7Ccn.bing.com%7C%7C%7C%7C%23',
        'Session': 'SmartLinkCode=51cto&SmartLinkKeyWord=&SmartLinkQuary=_UTF.&SmartLinkHost=blog.51cto.com&SmartLinkLanguage=zh',
        '_RF1': '139.226.176.169',
        '_bfa': '1.1622443080329.1gik74.1.1709048029542.1710597655733.35.1.101021',
        '_ubtstatus': '%7B%22vid%22%3A%221622443080329.1gik74%22%2C%22sid%22%3A35%2C%22pvid%22%3A1%2C%22pid%22%3A101021%7D',
        '_jzqco': '%7C%7C%7C%7C1710593260804%7C1.624638678.1708529546739.1710597647652.1710597655799.1710597647652.1710597655799.0.0.0.28.28',
        '_bfi': 'p1%3D101021%26p2%3D101021%26v1%3D1%26v2%3D2',
        '_bfaStatus': 'success',
    }
    df = pd.DataFrame(columns=np.arange(25))
    k = 0
    url='https://flights.ctrip.com/schedule/getScheduleByCityPair'
    for link in range(len(flight_link_2)): # 获取出发机场至到达机场及三级页面链接
        time.sleep(1)
        print("开始爬取"+flight_link_2[link].split("/")[-1].split(".")[0].upper()+"——"+flight_link_2[link].split(".")[-2].upper()+"航班")
        for num in range(2): #以北京至上海为例，最多2页航班数据，每页20个航班号
            headers = {
                'authority': 'flights.ctrip.com',
                'accept': 'application/json',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/json;charset=UTF-8',
                # 'cookie': '_RSG=4mKyJR3oQ2FL3D_FSXtBr8; _RDG=289fda7de3273426211d373ea0161b1ef2; _RGUID=f09ac836-d3f1-4c04-8d4b-de170ffcd0d5; MKT_CKID=1622443083256.9m8qg.vewg; _ga=GA1.2.707014534.1622443083; GUID=09031042214511715343; nfes_isSupportWebP=1; _bfaStatusPVSend=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217fb6f458bde18-07dae8d00d6fe-9771a3f-1296000-17fb6f458be72d%22%2C%22%24device_id%22%3A%2217fb6f458bde18-07dae8d00d6fe-9771a3f-1296000-17fb6f458be72d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fapp.mokahr.com%2F%22%2C%22%24latest_referrer_host%22%3A%22app.mokahr.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; __zpspc=9.25.1657444518.1657444870.4%233%7Ccn.bing.com%7C%7C%7C%7C%23; Session=SmartLinkCode=51cto&SmartLinkKeyWord=&SmartLinkQuary=_UTF.&SmartLinkHost=blog.51cto.com&SmartLinkLanguage=zh; _RF1=139.226.176.169; _bfa=1.1622443080329.1gik74.1.1709048029542.1710597655733.35.1.101021; _ubtstatus=%7B%22vid%22%3A%221622443080329.1gik74%22%2C%22sid%22%3A35%2C%22pvid%22%3A1%2C%22pid%22%3A101021%7D; _jzqco=%7C%7C%7C%7C1710593260804%7C1.624638678.1708529546739.1710597647652.1710597655799.1710597647652.1710597655799.0.0.0.28.28; _bfi=p1%3D101021%26p2%3D101021%26v1%3D1%26v2%3D2; _bfaStatus=success',
                'origin': 'https://flights.ctrip.com',
                'referer': 'https://flights.ctrip.com/schedule/'+ flight_link_2[link].split("/")[-1].split(".")[0].lower()+'.'+flight_link_2[link].split(".")[-2].lower()+'.html',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            }
            ploy_data = {
                        "departureCityCode": flight_link_2[link].split("/")[-1].split(".")[0].upper(), 
                        "arriveCityCode": flight_link_2[link].split(".")[-2].upper(),
                        "pageNo":num+1,
                        "departDate":"2024-02-26"
            }   #{"departureCityCode": "BJS", "arriveCityCode": "SHA"}

            try:
                response=requests.post(url=url,json=ploy_data,headers=headers,cookies=cookies).json()
            except:
                print(flight_link_2[link].split("/")[-1].split(".")[0].upper()+"——"+flight_link_2[link].split(".")[-2].upper()+"无航班！！")
                pass
            if k == 0:
                columns = []
                for key,value in response.get('scheduleVOList')[0].items():
                    if key == "currentWeekSchedule":
                        for x,y in value.items():
                            columns.append(key+x)
                    else:
                        columns.append(key)
                #print(columns)
                df.columns = columns
                k = 1

            for z in range(len(response.get('scheduleVOList'))):
                values = []
                for key,value in response.get('scheduleVOList')[z].items():
                    if key == "currentWeekSchedule":
                        for x,y in value.items():
                            values.append(y)
                    else:
                        values.append(value)
                #print(values)
                # df = df.append(pd.DataFrame([values], columns=df.columns))
                df=pd.concat([df,pd.DataFrame([values], columns=df.columns)])
        print(flight_link_2[link].split("/")[-1].split(".")[0].upper()+"——"+flight_link_2[link].split(".")[-2].upper()+"航班爬取完成！")
    return df

def main():
    # 获取所有机场及一级页面链接
    flight_name,flight_link = flight_departure()
    # 获取机场之间存在往返航班记录的机场数，以及二级页面链接
    flight_name_2, flight_link_2 = flight_dep_arr(flight_name,flight_link)
    df = flight_dep_arr_detail([link for link in flight_link_2 if 'bjs' in link.split('.')[0]])
    df.to_excel('携程航班数据-北京.xlsx',header=True)

if __name__=='__main__':
    main()