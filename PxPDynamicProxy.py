# -*- coding: utf-8 -*-
"""
Created on Mon Mar 8 10:15:00 2021

@author: Mohammad.FT
"""


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
