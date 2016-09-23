# Licensed under the Apache License, Version 2.0
from __future__ import division
import math
import os
import shelve


path = "/home/dell/B-Club/Analytics Geeks/Language Recognizer"
os.chdir(path)
s = shelve.open('data.ini', protocol = -1, writeback = True) # The data file

def createShelf():
  global s
  s['langs'] = dict()
  s['length'] = 0
  s['all'] = dict()
  s.sync()

def mkdict(path, encoding = 'utf-8'):
  global s
  import codecs
  import string
  temp = string.punctuation + ' ' + string.digits + '\n' + '\t'
  out = dict()
  out['words'] = dict()
  f = codecs.open(path, 'r', encoding)
  out['tot'] = 0
# out['totdiff'] = 0
  a = u'_'
  b = f.read(1)
  if (temp).encode(encoding).find(b) != -1 : b = f.read(1)
  c = f.read(1)
  if ((temp).encode(encoding).find(c) != -1  and c != u''): c = u'_'
  while c!= u'' and out['tot'] < 1000000:
    if (b != u'_' or (a == u'_' and c != u'_') or (a !=  u'_' and c == u'_')):
      try:
        out['words'][a+b+c] = out['words'][a+b+c] + 1
      except KeyError:
        out['words'][a+b+c] = 1
#       out['totdiff'] = out['totdiff'] + 1
    else:
      if (a == b and b == c) : out['tot'] = out['tot'] - 1
    a = b
    b = c
    c = f.read(1)
    if ((temp).encode('utf-8').find(c) != -1 and c != u'') : c = u'_'
    out['tot'] = out['tot'] + 1
  f.close()
  return out

def newLang(name, path, encoding = 'utf-8'): 
  global s
  if name in s['langs'] : return
  a = mkdict(path, encoding) 
  words = a['words'].iterkeys()
  s['langs'][name] = a['tot']
  s['length'] = s['length'] + 1
  for i in words:
    try:
      s['all'][i][name] = a['words'][i]
      if s['all'][i]['all'] <= a['words'][i] : s['all'][i]['all'] = a['words'][i]
    except KeyError:
      s['all'][i] = dict()
      s['all'][i][name] = a['words'][i]
      s['all'][i]['all'] = a['words'][i]
  s.sync()

def checkLang(path, encoding = 'utf-8'):
  global s
  dic = mkdict(path, encoding)
  check = dict()
  check['all'] = 0
  out = dict()
  for i in s['langs']:
    check[i] = 0
  words = dic['words'].iterkeys()
  for i in words:
    if i in s['all']:
      a = s['all'][i].iterkeys()
      for lang in a:
        if lang in s['langs']:
          try:
            b = (s['all'][i][lang] / s['all'][i]['all']) * (s['all'][i][lang] / s['langs'][lang])   / math.log(dic['tot'] / dic['words'][i])
          except:
            print "for", lang, i, s['all'][i][lang], s['all'][i]['all'], s['all'][i][lang], s['langs'][lang]
            b = 1
          check[lang] = check[lang] + b
          check['all'] = check['all'] + b
  for i in s['langs']:
    z = check[i] / check['all']
    if(z < (1/(2*s['length']))):
      check['all'] = check['all'] - check[i]
      check[i] = 0
  for i in s['langs']:
    out[i] = (check[i] / check['all']) * 100
  return out

try:
  s['all']
except KeyError:
  createShelf()

print "The languages available are:"
for i in s['langs']:
  print i
while(1):
  a = input("Hit 0 to check the language of a piece of text, 1 to add a new language to the tester or 9 to quit: ")
  if a == 0:
    b = raw_input("Enter the path to the piece of text: ")
    c = raw_input("Enter the encoding followed in the text. utf-8 preferred: ")
    d = checkLang(b, c)
    print "Language : Percentage"
    for i in d:
      print i + " : ", d[i]
  elif a == 1:
    print "I need a corporum which is at least 1,000,002 characters long to add a new language. Please download the same from any corporum on the internet and save it on the computer."
    b = raw_input("Enter the path to the corporum: ")
    c = raw_input("Enter the encoding followed in the text. utf-8 preferred: ")
    d = raw_input("Enter the name of the language: ")
    newLang(d, b, c)
    print "Language " + d + " added."
  else : break

print "Goodbye"
s.close()
