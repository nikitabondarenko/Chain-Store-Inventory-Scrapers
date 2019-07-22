# -*- coding: utf-8 -*-
import random
import base64
import urlparse
import logging
from scrapy.conf import settings


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        use_proxy = False
        proxies = settings.get("PROXIES")
        proxy_disabled_for = settings.get("PROXY_DISABLED_FOR")
        proxy_enabled_for = settings.get("PROXY_ENABLED_FOR")

        if proxy_disabled_for and proxy_enabled_for:
            use_proxy = False
            logging.warning("Only one of PROXY_DISABLED_FOR or PROXY_ENABLED_FOR parameters is allowed at the same time.")
        elif not proxy_disabled_for and not proxy_enabled_for:
            use_proxy = True
        elif proxy_disabled_for:
            host = urlparse.urlparse(request.url).netloc
            if host in proxy_disabled_for:
                logging.debug("Proxy disabled for " + host)
                use_proxy = False
            else:
                use_proxy = True
        elif proxy_enabled_for:
            host = urlparse.urlparse(request.url).netloc
            if host in proxy_enabled_for:
                logging.debug("Proxy enabled for " + host)
                use_proxy = True
            else:
                use_proxy = False

        if use_proxy and proxies:
            proxy_config = random.choice(proxies)
            host = proxy_config.get("host", None)
            login = proxy_config.get("login", None)
            password = proxy_config.get("password", None)

            if host:
                request.meta["proxy"] = host

            if login and password:
                encoded_user_pass = base64.encodestring(login + ":" + password)
                request.headers["Proxy-Authorization"] = "Basic " + encoded_user_pass


class SpiderProxyMiddleware(object):
    def process_request(self, request, spider):
        host = spider.proxy
#        login = proxy_config.get("login", None)
 #       password = proxy_config.get("password", None)

        if host:
            request.meta["proxy"] = host
        """
        if login and password:
            encoded_user_pass = base64.encodestring(login + ":" + password)
            request.headers["Proxy-Authorization"] = "Basic " + encoded_user_pass
        """

