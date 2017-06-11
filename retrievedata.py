#!/usr/bin/env python
#
# retrieve transaction data from web
#
# BeautifulSoup documentation from https://www.crummy.com/software/BeautifulSoup/bs4/doc/

import urllib
from bs4 import BeautifulSoup

url = "http://www.aigaogao.com/tools/history.html?s=000004"

html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

tags_a = soup('<span class="changeup">')
tags_td = soup('td')
"""
for tag in tags_a:
	print tag

for tag in tags_td:
	print tag
"""
print tags_a