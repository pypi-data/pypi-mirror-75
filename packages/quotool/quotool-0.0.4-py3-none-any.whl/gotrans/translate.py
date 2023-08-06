#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : taner
# @Date    : 2019/12/03 11:28
# @File    : translate.py

import requests
import execjs
import json
import enum


@enum.unique
class TranslateDirect(enum.IntEnum):
    English2Chinese = 1
    Chinese2English = 2


class GgTranslate:
    def __init__(self, text, dir: int):
        self.check_dir(dir)
        self.dir = dir

        self.base_url = 'https://translate.google.cn/translate_a/single'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }

        self.text = text

    def check_dir(self, dir):
        """
        检查方向
        :param dir:
        :return:
        """
        TranslateDirect(dir)

    def get_tk_param(self):
        """
        通过特别算法获取tk参数
        :return:
        """
        ctx = execjs.compile(""" 
            function TL(a) { 
                var k = ""; 
                var b = 406644; 
                var b1 = 3293161072;       
                var jd = "."; 
                var $b = "+-a^+6"; 
                var Zb = "+-3^+b+-f";    
                for (var e = [], f = 0, g = 0; g < a.length; g++) { 
                    var m = a.charCodeAt(g); 
                    128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : 
                    (55296 == (m & 64512) && g + 1 < a.length && 56320 == 
                    (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + 
                    ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
                    e[f++] = m >> 18 | 240, 
                    e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
                    e[f++] = m >> 6 & 63 | 128), 
                    e[f++] = m & 63 | 128) 
                } 
                a = b; 
                for (f = 0; f < e.length; f++) a += e[f], 
                a = RL(a, $b); 
                a = RL(a, Zb); 
                a ^= b1 || 0; 
                0 > a && (a = (a & 2147483647) + 2147483648); 
                a %= 1E6; 
                return a.toString() + jd + (a ^ b) 
            };

            function RL(a, b) { 
              var t = "a"; 
              var Yb = "+"; 
              for (var c = 0; c < b.length - 2; c += 3) { 
                  var d = b.charAt(c + 2), 
                  d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
                  d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
                  a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
              } 
              return a 
            } 
        """)

        tk = ctx.call('TL', self.text)
        return tk

    def get_param(self):
        """
        获取查询参数
        :return:
        """
        if TranslateDirect(self.dir) == TranslateDirect.English2Chinese:
            param_list = ['client=webapp',
                          'sl=auto',
                          'tl=zh-CN',
                          'hl=zh-CN',
                          'dt=at',
                          'dt=bd',
                          'dt=ex',
                          'dt=ld',
                          'dt=md',
                          'dt=qca',
                          'dt=rw',
                          'dt=rm',
                          'dt=ss',
                          'dt=t',
                          'source=bh',
                          'ssel=0',
                          'tsel=0',
                          'kc=1',
                          f'tk={self.get_tk_param()}',
                          f'q={self.text}'
                          ]
        elif TranslateDirect(self.dir) == TranslateDirect.Chinese2English:
            param_list = ['client=webapp',
                          'sl=auto',
                          'tl=en',
                          'hl=zh-CN',
                          'dt=at',
                          'dt=bd',
                          'dt=ex',
                          'dt=ld',
                          'dt=md',
                          'dt=qca',
                          'dt=rw',
                          'dt=rm',
                          'dt=ss',
                          'dt=t',
                          'dt=gt',
                          'ssel=0',
                          'tsel=3',
                          'kc=0',
                          f'tk={self.get_tk_param()}',
                          f'q={self.text}']

        param = '&'.join(param_list)

        return param

    def format_print(self, data):
        """
        格式化输出
        :return:
        """
        if data[1]:
            trans_set = {word_set[0]: word_set[1] for word_set in data[1]}
        else:
            trans_set = ""

        if TranslateDirect(self.dir) == TranslateDirect.English2Chinese:
            print('Chinese:', {data[0][0][0]}, trans_set)
        elif TranslateDirect(self.dir) == TranslateDirect.Chinese2English:
            print('English:', {data[0][0][0]}, trans_set)

    def run(self):
        """
        运行
        :return:
        """
        req_url = self.base_url + '?' + self.get_param()
        rls = requests.get(req_url, headers=self.headers)
        data = json.loads(rls.text)
        self.format_print(data)


def trans(words, direct=None):
    your_words = words if words else 'other'
    direction = direct if direct else int(TranslateDirect.English2Chinese)

    ggtl = GgTranslate(your_words, int(direction))
    ggtl.run()
