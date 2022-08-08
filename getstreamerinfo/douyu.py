# 获取斗鱼直播间的真实流媒体地址，默认最高画质
# 使用 https://github.com/wbt5/real-url/issues/185 中两位大佬@wjxgzz @4bbu6j5885o3gpv6ss8找到的的CDN，在此感谢！
import base64
import hashlib
import warnings
import re
import time

import execjs
import requests
from lxml import etree

class douyu():
    header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68",
        }
    header_mobile = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.100 Mobile Safari/537.36 '
        }
    host_list = ['tx2play1.douyucdn.cn','hdltctwk.douyucdn2.cn','akm-tct.douyucdn.cn','tc-tct1.douyucdn.cn']

    def __init__(self,rid:str) -> None:
        self.rid = rid

        self.did = '10000000000000000000000000001501'
        self.t10 = str(int(time.time()))
        self.t13 = str(int((time.time() * 1000)))

        self.s = requests.Session()
        self.res = self.s.get('https://m.douyu.com/' + str(rid)).text
        result = re.search(r'rid":(\d{1,8}),"vipId', self.res)

        if result:
            self.rid = result.group(1)
        else:
            raise Exception('房间号错误')
    
    @staticmethod
    def md5(data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def get_pre(self):
        url = 'https://playweb.douyucdn.cn/lapi/live/hlsH5Preview/' + self.rid
        data = {
            'rid': self.rid,
            'did': self.did
        }
        auth = douyu.md5(self.rid + self.t13)
        headers = {
            'rid': self.rid,
            'time': self.t13,
            'auth': auth
        }
        res = self.s.post(url, headers=headers, data=data).json()
        error = res['error']
        data = res['data']
        key = ''
        if data:
            rtmp_live = data['rtmp_live']
            key = re.search(r'(\d{1,8}[0-9a-zA-Z]+)_?\d{0,4}(/playlist|.m3u8)', rtmp_live).group(1)
        return error, key
    
    def is_available(self) -> bool:
        error, key = self.get_pre()
        if error == 102:
            return False
        else:
            return True

    def onair(self) -> bool:
        error, key = self.get_pre()
        if error not in [104,102]:
            return True
        else:
            return False

    def get_info(self):
        """
        return: title,uname,face_url,keyframe_url
        """
        room_url = 'https://www.douyu.com/' + self.rid
        response = requests.get(url=room_url, headers=self.header).text
        selector = etree.HTML(response)
        try:
            title = selector.xpath('//*[@id="js-player-title"]/div[1]/div[2]/div[1]/div[2]/div[1]/h3')[0].text
        except:
            title = 'huya'+self.rid
        try:
            uname = selector.xpath('//*[@id="js-player-title"]/div[1]/div[2]/div[2]/div[1]/div[2]/div/h2')[0].text
        except:
            uname = 'huya'+self.rid
        try:
            face_url = selector.xpath('//*[@id="js-player-title"]/div[1]/div[1]/div/a/div/img/@src')[0]
        except:
            face_url = None
        keyframe_url = None
        return title,uname,face_url,keyframe_url

