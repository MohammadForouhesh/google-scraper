# -*- coding: utf-8 -*-
"""
Created on Mon Mar 8 10:15:00 2021

@author: Mohammad.FT
"""

import urllib.request
import socket
import urllib.error
from termcolor import colored
from itertools import cycle


def set_proxy(driver, http_addr='', http_port=0, ssl_addr='', ssl_port=0, socks_addr='', socks_port=0):
    driver.execute("SET_CONTEXT", {"context": "chrome"})

    try:
        driver.execute_script("""
          Services.prefs.setIntPref('network.proxy.type', 1);
          Services.prefs.setCharPref("network.proxy.http", arguments[0]);
          Services.prefs.setIntPref("network.proxy.http_port", arguments[1]);
          Services.prefs.setCharPref("network.proxy.ssl", arguments[2]);
          Services.prefs.setIntPref("network.proxy.ssl_port", arguments[3]);
          Services.prefs.setCharPref('network.proxy.socks', arguments[4]);
          Services.prefs.setIntPref('network.proxy.socks_port', arguments[5]);
          """, http_addr, http_port, ssl_addr, ssl_port, socks_addr, socks_port)

    finally:
        driver.execute("SET_CONTEXT", {"context": "content"})


def is_bad_proxy(pip):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        request = urllib.request.Request('http://www.google.com')  # change the URL to test here
        socket = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:
        print("ERROR:", detail)
        return True
    return False


def refinery(proxy_path):
    proxy_file = open(proxy_path)
    doc = proxy_file.read()
    lines = doc.split('\n')
    proxy_iter = cycle(lines)
    proxy = next(proxy_iter)
    socket.setdefaulttimeout(1)
    i = 0

    with open("refined_proxy.txt", 'w') as refined:
        while i < len(lines):
            while is_bad_proxy(proxy):
                # print("Bad Proxy " + str(proxy))
                proxy = next(proxy_iter)
                i += 1
            print(colored(str(proxy) + " is working", 'green'))
            refined.writelines(proxy)
            refined.writelines("\n")
            proxy = next(proxy_iter)


if __name__ == '__main__':
    refinery("https10k_pxp.txt")