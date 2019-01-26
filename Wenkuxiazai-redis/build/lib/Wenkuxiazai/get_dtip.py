import requests
from lxml import etree
import re
import random
import time

def get_ip():
    ip_req = requests.get("动态ip的请求网址1")
    # print("1",ip_req.text)

    html = etree.HTML(ip_req.text)
    ip_list= html.xpath("//body/text()")[0].split("    ")
    # print("2", ip_list)
    ip_list2=[]
    ip_list3=[]
    ip_list4=[]
    for ip in ip_list:
        new_ip=ip.strip().split("s")
        # print(new_ip)
        ip_list2.append(new_ip)
        for i in new_ip:
            ip_list3.append(i)
    # print("3", ip_list3)
    for k in range(1,len(ip_list3),2):
        # print(k)
        if int(ip_list3[k])>30:
            ip_list4.append(ip_list3[k-1])
    # print("4", ip_list4)
    ip_proxies = []
    for i in ip_list4:
        # ip_proxies = 'http://dtip123456:dtip123456@' + ip_list[i] + ':888'
        ip_proxie = 'http://dtip123456:dtip123456@' + i + ':888'
        ip_proxies.append(ip_proxie)
    print('ip1_list',ip_proxies)
    if ip_proxies == [] or ip_proxies ==None:
        # time.sleep(1.5)
        # get_ip()
        return get_ip()
    else:
        return ip_proxies

def get_ip2():
    ip_req = requests.get("动态ip的请求网址2")
    # print("1",ip_req.text)

    html = etree.HTML(ip_req.text)
    ip_list= html.xpath("//body/text()")[0].split("    ")
    # print("2", ip_list)
    ip_list2=[]
    ip_list3=[]
    ip_list4=[]
    for ip in ip_list:
        new_ip=ip.strip().split("s")
        # print(new_ip)
        ip_list2.append(new_ip)
        for i in new_ip:
            ip_list3.append(i)
    # print("3", ip_list3)
    for k in range(1,len(ip_list3),2):
        # print(k)
        if int(ip_list3[k])>30:
            ip_list4.append(ip_list3[k-1])
    # print("4", ip_list4)
    ip_proxies = []
    for i in ip_list4:
        # ip_proxies = 'http://dtip123456:dtip123456@' + ip_list[i] + ':888'
        ip_proxie = 'http://dtip123456:dtip123456@' + i + ':888'
        ip_proxies.append(ip_proxie)
    print('ip1_list',ip_proxies)
    if ip_proxies == [] or ip_proxies == None:
        # time.sleep(1.5)
        return get_ip2()
    else:
        return ip_proxies
