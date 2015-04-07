#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import sys
import collections
try:
    from bs4 import BeautifulSoup
except ImportError:
    os.system('sudo pip install beautifulsoup4')
    from bs4 import BeautifulSoup

files = os.listdir('.')
contents_dir = filter(lambda x: x.endswith('_files'), files)[0]
os.chdir(contents_dir)
with open('campus.html') as f:
    html = f.read()
soup = BeautifulSoup(html)
os.chdir('..')

table = soup.find('table', {'class': 'normal'})
trs = table.find_all('tr')
points = {u'優上': 4.3, u'優': 4., u'良': 3., u'可': 2., u'不可': 0.}
credits = collections.defaultdict(int)
exception_flag = 0
for tr in trs[1:]:
    tds = tr.find_all('td')
    try:
        credit = float(tds[7].text)
        grade = tds[10].text
        credits[grade] += credit
    except Exception:
        if exception_flag == 1:
            continue
        print u'不可または未受験があります。'
        print u'不可はGPAにおそらく反映されるので注意してください。'
        print u'(不可は単位数がわからないので、このスクリプトは使えません)'
        exception_flag = 1

for grade, _ in sorted(points.items(), key=lambda x: x[1], reverse=True):
    print u'{}: {}'.format(grade, credits[grade])
sumof_credits = sum(credits[grade] for grade in points.keys())
print u'GPA換算単位数:', sumof_credits
gpa = sum(point * credits[grade] for grade, point in points.items())
gpa /= sumof_credits
print 'GPA:', gpa

