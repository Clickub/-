import csv
import requests
from lxml import etree
import time
import random

requests.packages.urllib3.disable_warnings()

numbers = 0
flag = 0
page_1 = 0
page_random = 2


def headers():
    global header
    Cookie = [

    ]
    User_Agent = [

    ]

    header = {
        'User-Agent': random.choice(User_Agent),
        'Cookie': random.choice(Cookie)
    }


def reminder():
    global flag
    flag += 1
    print(flag)


def delay(page):
    global page_1
    global page_random
    if page - page_1 == page_random:
        res = random.uniform(1.371, 2.862)
        time.sleep(res)
        page_1 = page
        page_random = random.randint(2, 7)


def write_head():
    result_headers = [
        '用户id',
        '微博昵称',
        #'微博正文',
        '是否认证',
        '是否会员',
        '有无签名',
        '微博数',
        '关注数',
        '粉丝数',
        '分组数',
        #'原创率',
        #'发图率',
        #'注册时间',
        '性别',
        '生日',
        '地区'
        #'参与话题数',
        #'@数',
        #'互相关注数'
    ]
    with open('路径', 'a',
              encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([result_headers])


def hot_id():
    headers()
    response = requests.get(url='https://m.weibo.cn/', headers=header, verify=False)  # 进入微博热门页面
    reminder()
    response_html = etree.HTML(response.text.encode('utf-8'))
    hot_href = response_html.xpath('//div[@class="m-text-box"]/a/@href')  # 获取热搜微博的用户
    hot_id = []
    for i in hot_href:
        hot_id.append(i[9:])
    return hot_id


def spider_user(user_list, content_list):
    global numbers
    for b, i in enumerate(user_list):
        headers()
        response = requests.get(url=i, headers=header, verify=False)
        reminder()
        response_html = etree.HTML(response.text.encode('utf-8'))
        id = response_html.xpath('//div[@class="ut"]/a[2]/@href')[0].split('/')[1]
        j = response_html.xpath('//td[@valign="top"]/div[@class="ut"]/span[@class="ctt"]/img/@alt')
        if len(j) == 0:
            iv = '0'
        else:
            if j[0] == 'V':
                iv = '1'
            else:
                iv = '0'
        k = response_html.xpath('//td[@valign="top"]/div[@class="ut"]/span[@class="ctt"]/a/img/@alt')
        if len(k) == 0:
            im = '0'
        else:
            im = '1'
        p = response_html.xpath('//span[@style="word-break:break-all; width:50px;"]/text()')
        if len(p) == 0:
            iw = '0'
        else:
            iw = '1'
        h = response_html.xpath('//div[@class="tip2"]//text()')
        weibo_num = h[0][3:][-2::-1][::-1]
        viewership = h[2][3:][-2::-1][::-1]
        fans_num = h[4][3:][-2::-1][::-1]
        group_num = h[6][3:][-2::-1][::-1]
        #viewership_each = str(spider_date(i))
        #forward_num = str(spider_forward(i))
        content = content_list[b]
        data_url = 'https://weibo.cn' + response_html.xpath('//div[@class="ut"]/a[2]/@href')[0]
        item = user_data(data_url)
        page = response_html.xpath('//input[@name="mp"]/@value')
        if len(page) == 0:
            pages_all = 1
        else:
            pages_all = int(page[0])
        url_new = i + '?page={}'.format(pages_all)
        headers()
        in_response = requests.get(url=url_new, headers=header, verify=False)
        reminder()
        in_html = etree.HTML(in_response.text.encode('utf-8'))
        weibo_id = in_html.xpath('//div[@class="c"]/@id')
        tap = len(weibo_id)
        if tap == 0:
            page = in_html.xpath('//input[@name="mp"]/@value')
            if len(page) == 0:
                pages_all = 1
            else:
                pages_all = int(page[0])
            url_new = i + '?page={}'.format(int(pages_all-pages_all*0.13))
            headers()
            in_response = requests.get(url=url_new, headers=header, verify=False)
            reminder()
            in_html = etree.HTML(in_response.text.encode('utf-8'))
            weibo_id = in_html.xpath('//div[@class="c"]/@id')
            tap = len(weibo_id)
        if len(weibo_id) == 0:
            registration_date = '0'
        else:
            registration_date = in_html.xpath('//div[@id="{}"]/div[last()]/span[@class="ct"]/text()'.format(weibo_id[-1]))[0][0:10]
        sum = tap + (pages_all-1)*10
        original_url = 'https://weibo.cn' + response_html.xpath('//div[@class="pms"]/a[1]/@href')[0]
        original_rate = format(original_pages(original_url)/sum, '.4f')
        picture_url = 'https://weibo.cn' + response_html.xpath('//div[@class="pms"]/a[2]/@href')[0]
        picture_rate = format(picture_pages(picture_url)/sum, '.4f')
        '''sum_1 = 0
        sum_2 = 0
        for page in range(1, pages + 1):
            if page == 1:
                comment_list = response_html.xpath('//span[@class="ctt"]/a/text()')
                for t in comment_list:
                    if '@' in t:
                        sum_1 += 1
                    if '#' in t:
                        sum_2 += 1
            else:
                delay(page)
                url_new = i + '?page={}'.format(page)
                headers()
                response = requests.get(url=url_new, headers=header, verify=False)
                reminder()
                response_html = etree.HTML(response.text.encode('utf-8'))
                comment_list = response_html.xpath('//span[@class="ctt"]/a/text()')
                for t in comment_list:
                    if '@' in t:
                        sum_1 += 1
                    if '#' in t:
                        sum_2 += 1'''
        #num_a = str(sum_1)
        #num_topic = str(sum_2)
        #num_original = str(int(weibo_num)-int(forward_num))
        result_data = []
        result_data.append(id)
        result_data.append(item['nickname'])
        result_data.append(content)
        result_data.append(iv)
        result_data.append(im)
        result_data.append(iw)
        result_data.append(weibo_num)
        result_data.append(viewership)
        result_data.append(fans_num)
        result_data.append(group_num)
        result_data.append(original_rate)
        result_data.append(picture_rate)
        result_data.append(registration_date)
        #result_data.append(forward_num)
        #result_data.append(num_original)
        result_data.append(item['gender'])
        result_data.append(item['birthday'])
        result_data.append(item['location'])
        #result_data.append(num_topic)
        #result_data.append(num_a)
        #result_data.append(viewership_each)
        with open('路径', 'a',
                  encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([result_data])
            numbers += 1
            print('已录入{}位用户信息'.format(numbers))
            time.sleep(2.18)


def spider_forward(url):
    headers()
    response = requests.get(url=url, headers=header, verify=False)
    reminder()
    response_html = etree.HTML(response.text.encode('utf-8'))
    page = response_html.xpath('//div[@class="pa"]/form/div/input/@value')
    if len(page) == 0:
        pages = 1
    else:
        pages = int(page[0])
    sum = 0
    for page in range(1, pages + 1):
        if page == 1:
            comment_list = response_html.xpath('//div[@class="c"]/div[1]/span[@class="cmt"]/text()[1]')
            for i in comment_list:
                if '转发了' in i:
                    sum += 1
        else:
            delay(page)
            url_new = url + '?page={}'.format(page)
            headers()
            response = requests.get(url=url_new, headers=header, verify=False)
            reminder()
            response_html = etree.HTML(response.text.encode('utf-8'))
            comment_list = response_html.xpath('//div[@class="c"]/div[1]/span[@class="cmt"]/text()[1]')
            for i in comment_list:
                if '转发了' in i:
                    sum += 1
    return sum


def spider_date(url):
    headers()
    response = requests.get(url=url, headers=header, verify=False)
    reminder()
    response_html = etree.HTML(response.text.encode('utf-8'))
    href_list = response_html.xpath('//div[@class="tip2"]/a/@href')
    url_1 = 'https://weibo.cn' + href_list[0]
    headers()
    info_1 = requests.get(url=url_1, headers=header, verify=False)
    reminder()
    info_1_html = etree.HTML(info_1.text.encode('utf-8'))
    h = []
    page = info_1_html.xpath('//input[@name="mp"]/@value')
    if len(page) == 0:
        pages = 1
    else:
        pages = int(page[0])
    for page in range(1, pages + 1):
        if page == 1:
            table_1 = info_1_html.xpath('//td[@valign="top"]/a[1]/text()')
            for j in table_1:
                h.append(j)
        else:
            delay(page)
            url_new = url_1 + '?page={}'.format(page)
            headers()
            info_1 = requests.get(url=url_new, headers=header, verify=False)
            reminder()
            info_1_html = etree.HTML(info_1.text.encode('utf-8'))
            table_1 = info_1_html.xpath('//td[@valign="top"]/a[1]/text()')
            for j in table_1:
                h.append(j)

    url_2 = 'https://weibo.cn/' + href_list[1]
    headers()
    info_2 = requests.get(url=url_2, headers=header, verify=False)
    reminder()
    info_2_html = etree.HTML(info_2.text.encode('utf-8'))
    k = []
    page = info_2_html.xpath('//input[@name="mp"]/@value')
    if len(page) == 0:
        pages = 1
    else:
        pages = int(page[0])
    for page in range(1, pages + 1):
        if page == 1:
            table_2 = info_2_html.xpath('//td[@valign="top"]/a[1]/text()')
            for j in table_2:
                k.append(j)
        else:
            delay(page)
            url_new = url_2 + '?page={}'.format(page)
            headers()
            info_2 = requests.get(url=url_new, headers=header, verify=False)
            reminder()
            info_2_html = etree.HTML(info_2.text.encode('utf-8'))
            table_2 = info_2_html.xpath('//td[@valign="top"]/a[1]/text()')
            for j in table_2:
                k.append(j)

    sum = 0
    for i in h:
        for j in k:
            if j == i:
                sum += 1
                k.remove(j)
                break
    return sum


def spider_in(url_list):
    for url in url_list:
        headers()
        response = requests.get(url=url, headers=header, verify=False)
        reminder()
        response_html = etree.HTML(response.text.encode('utf-8'))
        page = response_html.xpath('//input[@name="mp"]/@value')
        if len(page) == 0:
            pages = 1
        else:
            pages = int(page[0])
        for page in range(1, pages + 1):
            if page == 1:
                id_list = response_html.xpath('//div[@class="c"]/@id')
                del id_list[0]
                if len(id_list) == 0:
                    break
                for id in id_list:
                    comment = response_html.xpath('//div[@id="{}"]/span[@class="ctt"]/text()'.format(id))
                    contents = []
                    content = ''.join(comment)
                    contents.append(content)
                    user_list = response_html.xpath('//div[@id="{}"]/a[1]/@href'.format(id))
                    for i, k in enumerate(user_list):
                        user_list[i] = 'https://weibo.cn' + k
                    spider_user(user_list, contents)
            else:
                delay(page)
                url_new = url.split('#cmtfrm')[0] + '&page={}'.format(page)
                headers()
                response = requests.get(url=url_new, headers=header, verify=False)
                reminder()
                response_html = etree.HTML(response.text.encode('utf-8'))
                id_list = response_html.xpath('//div[@class="c"]/@id')
                del id_list[0]
                if len(id_list) == 0:
                    break
                for id in id_list:
                    comment = response_html.xpath('//div[@id="{}"]/span[@class="ctt"]/text()'.format(id))
                    contents = []
                    content = ''.join(comment)
                    contents.append(content)
                    user_list = response_html.xpath('//div[@id="{}"]/a[1]/@href'.format(id))
                    for i, k in enumerate(user_list):
                        user_list[i] = 'https://weibo.cn' + k
                    spider_user(user_list, contents)


def user_data(url):
    item = {
        'nickname': '0',
        'gender': '0',
        'birthday': '0',
        'location': '0'
    }
    headers()
    response = requests.get(url=url, headers=header, verify=False)
    response_html = etree.HTML(response.text.encode('utf-8'))
    data_text = response_html.xpath('/html/body/div[7]/text()')
    item['birthday'] = '0'
    for i in data_text:
        if '生日' in i:
            item['birthday'] = i[3:]
        if '性别' in i:
            item['gender'] = i[3:]
        if '地区' in i:
            item['location'] = i[3:]
        if '昵称' in i:
            item['nickname'] = i[3:]
    return item


def original_pages(url):
    headers()
    response = requests.get(url=url, headers=header, verify=False)
    reminder()
    response_html = etree.HTML(response.text.encode('utf-8'))
    page = response_html.xpath('//input[@name="mp"]/@value')
    if len(page) == 0:
        pages = 1
    else:
        pages = int(page[0])
    url_new = url + '?page={}'.format(pages)
    headers()
    in_response = requests.get(url=url_new, headers=header, verify=False)
    reminder()
    in_html = etree.HTML(in_response.text.encode('utf-8'))
    tap = len(in_html.xpath('//div[@class="c"]/@id'))
    sum = tap + (pages - 1) * 10
    return sum


def picture_pages(url):
    headers()
    response = requests.get(url=url, headers=header, verify=False)
    reminder()
    response_html = etree.HTML(response.text.encode('utf-8'))
    page = response_html.xpath('//input[@name="mp"]/@value')
    if len(page) == 0:
        pages = 1
    else:
        pages = int(page[0])
    url_new = url + '?page={}'.format(pages)
    headers()
    in_response = requests.get(url=url_new, headers=header, verify=False)
    reminder()
    in_html = etree.HTML(in_response.text.encode('utf-8'))
    tap = len(in_html.xpath('//div[@class="c"]/@id'))
    sum = tap + (pages - 1) * 10
    return sum


def main():

    write_head()   #写入数据头部

    while True:
        id = hot_id()
        for i in id:
            headers()
            response = requests.get(url='https://weibo.cn/{}'.format(i), headers=header, verify=False)
            reminder()
            response_html = etree.HTML(response.text.encode('utf-8'))
            comment_list = response_html.xpath('//div[@class="c"]/div[last()]/a[last()-1]/@href')
        for i in comment_list:
            headers()
            response = requests.get(url=i, headers=header, verify=False)
            reminder()
            response_html = etree.HTML(response.text.encode('utf-8'))
            comment_list = response_html.xpath('//div[@class="c"]/div[last()]/a[last()-1]/@href')
        headers()
        response = requests.get(url='https://weibo.cn/search/?pos=search', headers=header, verify=False)   #进入微博搜索页面
        reminder()
        response_html = etree.HTML(response.text.encode('utf-8'))
        hot_href = response_html.xpath('/html/body/div[7]/a/@href')   #获取热搜微博的网址
        for i in hot_href:
            headers()
            in_response = requests.get(url='https://weibo.cn{}'.format(i), headers=header, verify=False)   #依次进入获取的热搜网址
            reminder()
            in_html = etree.HTML(in_response.text.encode('utf-8'))
            page = in_html.xpath('//input[@name="mp"]/@value')   #获取页数
            if len(page) == 0:
                pages = 1
            else:
                pages = int(page[0])
            for page in range(1, pages+1):
                if page == 1:
                    user_list = in_html.xpath('//a[@class="nk"]/@href')   #获取该页的发帖用户网址
                    id_list = in_html.xpath('//div[@class="c"]/@id')   #获取该页贴子的id
                    contents = []
                    for id in id_list:
                        comment = in_html.xpath('/html/body/div[@id="{}"]/div/span[@class="ctt"]/text()'.format(id))   #依次获取id的评论信息
                        content = ''.join(comment)
                        contents.append(content)
                        comment_href = in_html.xpath('/html/body/div[@id="{}"]/div[last()]/a[last()-1]/@href'.format(id))   #依次获取该页各帖子的评论区网址
                        spider_in(comment_href)   #处理评论区
                    spider_user(user_list, contents)   #处理用户信息
                else:
                    delay(page)
                    url='https://weibo.cn' + i + '&page={}'.format(page)
                    headers()
                    in_response = requests.get(url=url, headers=header, verify=False)
                    reminder()
                    in_html = etree.HTML(in_response.text.encode('utf-8'))
                    user_list = in_html.xpath('//a[@class="nk"]/@href')
                    id_list = in_html.xpath('div[@class="c"]/@id')
                    contents = []
                    for id in id_list:
                        comment = in_html.xpath('//div[@id="{}"]/div/span[@class="ctt"]/text()'.format(id))
                        content = ''.join(comment)
                        contents.append(content)
                        comment_href = in_html.xpath('//div[@id="{}"]/div[last()]/a[last()-1]/@href'.format(id))
                        spider_in(comment_href)
                    spider_user(user_list, contents)


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            main()


