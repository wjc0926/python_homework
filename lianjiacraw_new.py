# from bs4 import BeautifulSoup
# import requests
# from urllib import request
# import os
#
#
# def getHouseList(url):
#     house = []
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
#     }
#     # 禁用代理
#     proxies = {
#         "http": None,
#         "https": None,
#     }
#
#     # get 从网页获取信息
#     res = requests.get(url, headers=headers, proxies=proxies)
#     # 解析内容, 使用 BeautifulSoup 解析 HTML 内容
#     soup = BeautifulSoup(res.content, 'lxml')
#
#     # 房源 title
#     housename_divs = soup.find_all('div', class_='title')
#     for housename_div in housename_divs:
#         housename_as = housename_div.find_all('a')
#         for housename_a in housename_as:
#             housename = []
#             # 标题
#             housename.append(housename_a.get_text())
#             # 超链接
#             if 'href' in housename_a.attrs:
#                 housename.append(housename_a['href'])
#             else:
#                 housename.append(None)
#             house.append(housename)
#
#     # 房源具体信息
#     huseinfo_divs = soup.find_all('div', class_='houseInfo')
#     for i in range(len(huseinfo_divs)):
#         info = huseinfo_divs[i].get_text()
#         infos = info.split('|')
#         # 户型
#         house[i].append(infos[0])
#         # 平米
#         house[i].append(infos[1])
#         # 朝向
#         house[i].append(infos[2])
#         # 装修风格
#         house[i].append(infos[3])
#
#     # 小区名和地址
#     position_info_divs = soup.find_all('div', class_='positionInfo')
#     for i in range(len(position_info_divs)):
#         position_info = position_info_divs[i]
#         community_name = position_info.find_all('a')[0].get_text()
#         address = position_info.get_text().strip()
#         house[i].append(community_name)
#         house[i].append(address)
#
#     # 关注人数和发布时间
#     follow_info_divs = soup.find_all('div', class_='followInfo')
#     for i in range(len(follow_info_divs)):
#         follow_info = follow_info_divs[i].get_text().strip()
#         house[i].append(follow_info)
#
#     # 总价和单价
#     price_info_divs = soup.find_all('div', class_='priceInfo')
#     for i in range(len(price_info_divs)):
#         total_price = price_info_divs[i].find('div', class_='totalPrice').find('span').get_text().strip()
#         unit_price = price_info_divs[i].find('div', class_='unitPrice').find('span').get_text().strip()
#         house[i].append(total_price)
#         house[i].append(unit_price)
#
#     # 保存图片
#     img_divs = soup.find_all('a', class_='noresultRecommend img LOGCLICKDATA')
#     for i in range(len(img_divs)):
#         img_tag = img_divs[i].find('img', class_='lj-lazy')
#         if img_tag and 'data-original' in img_tag.attrs:
#             img_url = img_tag['data-original']
#             if img_url:
#                 img_filename = f"house_{i}.jpg"
#                 img_path = os.path.join('images', img_filename)
#                 if not os.path.exists('images'):
#                     os.makedirs('images')
#                 request.urlretrieve(img_url, img_path)
#                 house[i].append(img_path)
#
#     return house
#
#
# def appendHouse(url):
#     houses = getHouseList(url)
#     for house in houses:
#         print(house)
#
#
# def getShengShiChangAn():
#     for i in range(1, 4):
#         print('-----分隔符', i, '-------')
#         if i == 1:
#             url = 'https://sjz.lianjia.com/ershoufang/c3211056507395/?sug=%E7%9B%9B%E4%B8%96%E9%95%BF%E5%AE%89'
#         else:
#             url = 'https://sjz.lianjia.com/ershoufang/pg' + str(
#                 i) + 'c3211056507395/?sug=%E7%9B%9B%E4%B8%96%E9%95%BF%E5%AE%89'
#         appendHouse(url)
#
#
# # 主函数
# def main():
#     getShengShiChangAn()
#
#
# if __name__ == '__main__':
#     main()

from bs4 import BeautifulSoup
import requests
from urllib import request
import os
import csv


def getHouseList(url, page_number):
    house_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }
    # 禁用代理
    proxies = {
        "http": None,
        "https": None,
    }

    try:
        # get 从网页获取信息
        res = requests.get(url, headers=headers, proxies=proxies)
        res.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return house_list  # 返回空列表

    # 解析内容, 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(res.content, 'lxml')

    # 房源 title
    housename_divs = soup.find_all('div', class_='title')
    for housename_div in housename_divs:
        housename_as = housename_div.find_all('a')
        for housename_a in housename_as:
            housename = []
            # 标题
            housename.append(housename_a.get_text().strip())
            # 超链接
            if 'href' in housename_a.attrs:
                housename.append(housename_a['href'])
            else:
                housename.append(None)
            house_list.append(housename)

    # 房源具体信息
    huseinfo_divs = soup.find_all('div', class_='houseInfo')
    for i in range(len(huseinfo_divs)):
        info = huseinfo_divs[i].get_text()
        infos = info.split('|')
        # 户型
        house_list[i].append(infos[0].strip())
        # 平米
        house_list[i].append(infos[1].strip())
        # 朝向
        house_list[i].append(infos[2].strip())
        # 装修风格
        house_list[i].append(infos[3].strip())

    # 小区名和地址
    position_info_divs = soup.find_all('div', class_='positionInfo')
    for i in range(len(position_info_divs)):
        position_info = position_info_divs[i]
        community_name = position_info.find_all('a')[0].get_text().strip()
        address_parts = position_info.find_all('a')
        address = " ".join([part.get_text().strip() for part in address_parts[1:]])
        house_list[i].append(community_name)
        house_list[i].append(address)

    # 关注人数和发布时间
    follow_info_divs = soup.find_all('div', class_='followInfo')
    for i in range(len(follow_info_divs)):
        follow_info = follow_info_divs[i].get_text().strip()
        house_list[i].append(follow_info)

    # 总价和单价
    price_info_divs = soup.find_all('div', class_='priceInfo')
    for i in range(len(price_info_divs)):
        total_price = price_info_divs[i].find('div', class_='totalPrice').find('span').get_text().strip()
        unit_price = price_info_divs[i].find('div', class_='unitPrice').find('span').get_text().strip()
        house_list[i].append(total_price)
        house_list[i].append(unit_price)

    # 保存图片
    img_divs = soup.find_all('a', class_='noresultRecommend img LOGCLICKDATA')
    for i in range(len(img_divs)):
        img_tag = img_divs[i].find('img', class_='lj-lazy')
        if img_tag and 'data-original' in img_tag.attrs:
            img_url = img_tag['data-original']
            if img_url:
                img_filename = f"house_{page_number}_{i}.jpg"
                img_path = os.path.join('images', img_filename)
                if not os.path.exists('images'):
                    os.makedirs('images')
                request.urlretrieve(img_url, img_path)
                house_list[i].append(img_path)

    return house_list

def appendHouse(url, writer, page_number):
    houses = getHouseList(url, page_number)
    for house in houses:
        writer.writerow(house)

def getShengShiChangAn():
    with open('houses_new.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(
            ["房源标题", "链接", "户型", "面积", "房屋朝向", "装修形式", "小区名称", "地址", "关注度",
             "总价", "单价", "图片路径"])
        for i in range(1, 51):
            print('-----分隔符', i, '-------')
            if i == 1:
                url = 'https://xm.lianjia.com/ershoufang/'
            else:
                url = f'https://xm.lianjia.com/ershoufang/pg{i}/'
            appendHouse(url, writer, i)

# 主函数
def main():
    getShengShiChangAn()

if __name__ == '__main__':
    main()


