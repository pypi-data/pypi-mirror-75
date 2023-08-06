# -*- encoding: utf-8 -*-
import requests
import json


__method__ = ['getAddressByIp', 'getSampleAddressByIp', 'getUserAgent']
__author__ = u'seal'


def getMethod():
    return __method__


def getAddressByIp(ip):
    """
    通过ip地址获取归属地以及其他详细信息
    """
    if not isinstance(ip, str) and not isinstance(ip, unicode):
        raise ValueError('ipaddress must be str')
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query={}&resource_id=6006'.format(ip)
    try:
        html = requests.get(url=url, headers=headers).text
        data = json.loads(html)
    except Exception as e:
        return 'time error'
    return data


def getSampleAddressByIp(ip):
    """
    通过ip地址获取归属地
    """
    data = getAddressByIp(ip)
    if isinstance(data, dict):
        try:
            data = data['data'][0]['location']
        except:
            return 'time error'
    return data


def getUserAgent():
    """
    返回一个User-Agent
    """
    return 'Mozilla/5.0'


if __name__ == '__main__':
    pass
