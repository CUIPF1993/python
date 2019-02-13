#!/usr/bin/env python
# encoding: utf-8

"""
@version: python3.6
@author:  CPF 
@contact: cpfyjjs@foxmail.com
@site: 
@software: PyCharm Community Edition
@file: zhihu_answer.py
@time: 2017/7/28 23:15
"""

import requests
from urllib.parse import urlencode
import json
import re


#url = 'https://www.zhihu.com/api/v4/questions/27726057/answers?'
#问题连接url
url = 'https://www.zhihu.com/api/v4/questions/19942050/answers?'
headers = {
'User-Agent':'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
}


def get_html(url,offset,limit):
    '''
    获取详情页的内容
    :param url: 请求连接
    :param offset:
    :param limit:
    :return: 详情页内容。
    '''
    data = {
        'include': 'data[*].is_normal,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].author.follower_count,badge[?(type=best_answerer)].topics',
        'offset': offset,
        'limit': limit,
        'sort_by': 'default'
    }
    url = url+ urlencode(data)
    try:
        response = requests.get(url,headers = headers)
        response.encoding = response.apparent_encoding
        response.raise_for_status()
        result = response.text
        return result
    except:
        print('爬去失败')

def parse_html(html):
    data = json.loads(html)
    if data.get('data'):
        items = data.get('data')
        for item in items:
            text = item.get('content')
            #将<>标签替换为换行符
            result, number = re.subn(re.compile('<.*?>'),'\n',text)
            yield result

if __name__ == '__main__':
    #以utf-8编码打开一个文件
    with open('zhihu2.txt','w',encoding='utf-8') as f:
        for i in range(100):
            offset = 10*i + 3
            #不断翻页获取数据
            html = get_html(url,offset,20)
            for text in parse_html(html):
                f.write(text)
                f.write('\n')
    print('爬虫爬去完毕')




