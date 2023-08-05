#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
from six.moves.urllib import request
import requests
import json
import random
import time
import datetime
from loguru import logger
from amz_query.request_conf import COM, CA, UK, DE, USER_AGENTS
import collections

logger.add("request.log", rotation="500 MB")

Response = collections.namedtuple('Response',['html','error','ip']) 


class AmazonRequest():


    def __init__(self, cookies_com=[],
                       cookies_ca=[],
                       cookies_uk=[],
                       cookies_de=[],
                       retry=1):

        self.COM = COM
        self.CA = CA
        self.UK = UK
        self.DE = DE
        self.USER_AGENTS = USER_AGENTS



        if cookies_com: self.COM = cookies_com
        if cookies_ca: self.CA = cookies_ca
        if cookies_uk: self.UK = cookies_uk
        if cookies_de: self.DE = cookies_de

        self.head = {
                    'authority': 'www.amazon.ca',
                    'method': 'GET',
                    'scheme': 'https',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en,en-US;q=0.9',
                    'cache-control': 'max-age=0',
                    'cookie': random.choice(self.COM),
                    'downlink':'10',
                    'ect': '4g',
                    'rtt': '100',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'service-worker-navigation-preload': 'true',
                    'upgrade-insecure-requests': '1',
                    'user-agent':random.choice(self.USER_AGENTS)}
        
        
        
        self.proxies = {}

        self.session = requests.session()
        
        self.retry = retry
        
        self.ip = {}
        
        self.error = {"request_error": "",
                      "proxy_error": "",}


    def proxy(self):
        r1 = datetime.datetime.now()

        opener = request.build_opener(
            request.ProxyHandler(self.proxies))
        try:
            self.ip = json.loads(opener.open('http://lumtest.com/myip.json', timeout=5).read())

            addr = self.ip["ip"]
            country = self.ip["country"]

            logger.info(f"Current IP: {addr} - IP Location: {country}")

        except Exception as e:
            self.error['proxy_error'] = str(e)

        r2 = datetime.datetime.now()

        ti = (r2 - r1).seconds
        
        logger.info(f"Get Proxy Time: {ti} seconds")

        return self.ip

    def request_(self, **kwargs):
        for i in range(self.retry):
            try:
                if kwargs.get('data'):
                    res = self.session.post(
                        timeout=20, proxies=self.proxy(), **kwargs)
                    assert res.status_code == 200
                    return BeautifulSoup(res.content, 'lxml')
                else:
                    c1 = datetime.datetime.now()
                    
                    res =self.session.get(timeout=15, proxies=self.proxy(), **kwargs)

                    c2 = datetime.datetime.now()

                    ti = (c2 - c1).seconds

                    logger.info(f"Request Time: {ti} seconds | Status: {res.status_code}")
                    
                    # request back nothing from amazon
                    if res == None:
                        logger.info('Not content, after 2 seconds will continue query')
                        time.sleep(2)
                        continue
                    
                    # request fail cause robot check
                    if 'Sorry! Something went wrong!' in res.text or "make sure you're not a robot" in res.text:
                        logger.info('Sorry content, after 2 seconds will continue query')
                        time.sleep(2)
                        continue

                    return BeautifulSoup(res.content, 'html5lib')

            except Exception as e:
                logger.info(f"request error - reason - {e}")
                time.sleep(5)
            else:
                break
        else:
            return ''
            
    
    def amazon_request(self, url):
        
        self.url = url
        
        # update location by asin url
        proxy_loc = "us"

        if 'www.amazon.ca' in self.url:
            self.head.update({"cookie": random.choice(self.CA)})
            proxy_loc = "ca"
            
        if 'www.amazon.co.uk' in self.url:
            self.head.update({"cookie": random.choice(self.UK)})
            proxy_loc = "uk"
            
        if 'www.amazon.de' in self.url:
            self.head.update({"cookie": random.choice(self.DE)})
            proxy_loc = "de"
        
        
        # update proxy by location
        proxy_seed = random.randint(1000, 2000)
        
        if proxy_loc:
            self.proxy_loc = f"country-{proxy_loc}-"
        else:
            self.proxy_loc = ""

        self.proxies = {'http': 'http://lum-customer-hl_2cfe73d0-zone-static-{}session-{}:jxen5us71prn@zproxy.lum-superproxy.io:22225'.format(
                        self.proxy_loc, proxy_seed),
                      'https': 'http://lum-customer-hl_2cfe73d0-zone-static-{}session-{}:jxen5us71prn@zproxy.lum-superproxy.io:22225'.format(
                        self.proxy_loc, proxy_seed)}
        
        # request content
        content = self.request_(url=self.url, headers=self.head)
        res = Response(html=content, error=self.error, ip=self.ip)
        return res




if __name__ == '__main__':
    res = AmazonRequest().amazon_request(URL)






