# -*- coding: utf-8 -*-
import vim,urllib,re,collections,xml.etree.ElementTree as ET
import sys,json

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError

def str_encode(word):
    if sys.version_info >= (3, 0):
        return word
    else:
        return word.encode('utf-8')

def str_decode(word):
    if sys.version_info >= (3, 0):
        return word
    else:
        return word.decode('utf-8')

def bytes_decode(word):
    if sys.version_info >= (3, 0):
        return word.decode()
    else:
        return word

def bytes_encode(word):
    if sys.version_info >= (3, 0):
        return word.encode('utf-8')
    else:
        return word

def url_quote(word):
    if sys.version_info >= (3, 0):
        return urllib.parse.quote(word)
    else:
        return urllib.quote(word.encode('utf-8'))

QUERY_BLACK_LIST = ['.', '|', '^', '$', '\\', '[', ']', '{', '}', '*', '+', '?', '(', ')', '&', '=', '\"', '\'', '\t']

def preprocess_word(word):
    word = word.strip()
    for i in QUERY_BLACK_LIST:
        word = word.replace(i, ' ')
    array = word.split('_')
    word = []
    p = re.compile('[a-z][A-Z]')
    for piece in array:
        lastIndex = 0
        for i in p.finditer(piece):
            word.append(piece[lastIndex:i.start() + 1])
            lastIndex = i.start() + 1
        word.append(piece[lastIndex:])
    return ' '.join(word).strip()

def get_query_url(query):
    import hashlib
    import random
    appid = vim.eval("g:baidu_appid")
    secretKey = vim.eval("g:baidu_secretKey")

    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    fromLang = 'auto'
    toLang = 'auto'
    salt = random.randint(32768, 65536)

    sign = appid+query+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+url_quote(query)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    return myurl

def get_opener():
    proxy_handler = urllib.request.ProxyHandler(proxies)
    proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
    opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
    return opener

def query_from_baidu(query):
    try:
        word = preprocess_word(query)
        if not word:
            return ''
        url = get_query_url(word)
        r = urlopen(url)
    except IOError:
        return 'NETWORK_ERROR'

    response = json.loads(bytes_decode(r.read()))
    if response.get('error_code') is not None:
        return response.get('error_msg')

    response = response.get('trans_result')
    result = ''
    if response is not None and len(response) > 0:
        for i in response:
            result = result + i.get('dst') + "\n"
        return result
    else:
        return 'NO_RESULT'

def baidu_translate_visual_selection(lines):
    lines = str_decode(lines)
    appid = vim.eval("g:baidu_appid")
    info = query_from_baidu(lines)
    
    vim.command('let @"="'+ info.replace('\n', '') +'"')
    for line in info.split('\n'):
        vim.command('echo "'+ line +'"')

