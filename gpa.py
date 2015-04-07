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
grades = [u'優上', u'優', u'良', u'可', u'不可'] 
points = dict(zip(grades, [4.3, 4., 3., 2., 0.]))
credits = collections.defaultdict(int)
for tr in trs[1:]:
    tds = tr.find_all('td')
    credit =  float(tds[7].text)
    grade = tds[10].text
    credits[grade] += credit
for grade in grades:
    print u'{}: {}'.format(grade, credits[grade])
sumof_credits = sum(credit for grade, credit in credits.items()
                    if grade in points)
print u'GPA換算単位数:', sumof_credits
gpa = sum(point * credits[grade] for grade, point in points.items())
gpa /= sumof_credits
print 'GPA:', gpa

