# -*- coding: utf-8 -*-

import re
import MySQLdb
from lxml.html import parse

RSS_LIST = ["http://www.lemonde.fr/rss/sequence/0,2-3210,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3214,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3224,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3234,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3236,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3238,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3242,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3244,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3246,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-651865,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3476,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3546,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3260,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3404,1-0,0.xml",
        "http://www.lemonde.fr/rss/sequence/0,2-3232,1-0,0.xml",
        ]

DB_HOST = "localhost"
DB_USER = "frenchwords"
DB_PASS = "bonjour"
DB_NAME = "frenchwords"


__db = MySQLdb.connect(host=DB_HOST ,user=DB_USER ,passwd=DB_PASS,db=DB_NAME, charset = "utf8", use_unicode = True)
__db.autocommit(True)
cur = __db.cursor()


"""
CREATE TABLE `frenchwords`.`words` (
  `id` INT  NOT NULL AUTO_INCREMENT,
  `word` VARCHAR(100)  NOT NULL,
  `wordcount` INT  NOT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = MyISAM
CHARACTER SET utf8 COLLATE utf8_general_ci;


"""

def count_words(url):
    doc = parse(url).getroot()
    paragraphs = []

    for text in doc.cssselect('body p'):
        paragraphs.append(text.text)

    for text in doc.cssselect('body p.firstLine'):
        paragraphs.append(text.text)

    split_lines = []
    for line in paragraphs:
        try:
            split_lines.append(line.split(' '))
        except:
            print "Error"


        words = []
        r1 = re.compile(r"[a-z]+'")
        for line in split_lines:
            for word in line:
                word = word.replace(',', '')
                word = word.replace('.', '')
                word = word.replace(' ', '')
                word = word.replace('"', '')
                word = word.replace('(', '')
                word = word.replace(')', '')
                word = word.replace('-', '')
                match = r1.match(word)
                if match:
                    b = r1.split(word)
                    word = b[1]
                if len(word) > 3:
                    word = word.replace("'", '')
                    words.append(word.lower())
    return words

if __name__ == "__main__":
    import xml.dom.minidom
    import urllib
    from time import sleep
    for url in RSS_LIST:
        webFile = urllib.urlopen(url).read()
        dom = xml.dom.minidom.parseString(webFile)
        links =  dom.getElementsByTagName("link")
        link_list = []
        for link in links[2:]:
            sleep(2)
            lst = count_words(link.firstChild.data)
            word_count = [(a, lst.count(a)) for a in set(lst)]
            for word in word_count:
                print "%s: %i" % (word[0].encode("utf-8"), word[1])
                query = "select * from words where word = '%s'" % word[0]
                cur.execute(query)
                if cur.rowcount == 1:
                    query = "update words set wordcount = wordcount + %i where word = '%s'" % (word[1], word[0])
                elif cur.rowcount == 0:
                    query = "insert into words values (NULL,'%s',%i)" % (word[0], word[1])
                else:
                    raise Exception
                cur.execute(query)