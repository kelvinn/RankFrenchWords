import MySQLdb
import csv
import translatejson
from time import sleep

DB_HOST = "localhost"
DB_USER = "frenchwords"
DB_PASS = "bonjour"
DB_NAME = "frenchwords"

__db = MySQLdb.connect(host=DB_HOST ,user=DB_USER ,passwd=DB_PASS,db=DB_NAME, charset = "utf8", use_unicode = True)
__db.autocommit(True)
cur = __db.cursor()



"""
CREATE TABLE `frtoenwords`.`words` (
  `id` INT  NOT NULL AUTO_INCREMENT,
  `fr` VARCHAR(100)  CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `en` VARCHAR(100)  NOT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = MyISAM
CHARACTER SET utf8 COLLATE utf8_general_ci;

"""

wordWriter = csv.writer(open('wordlist.csv', 'w'), delimiter=' ',
                         quotechar='|', quoting=csv.QUOTE_MINIMAL)

query = "select * from words where wordcount < 15 order by wordcount DESC limit 3000"
cur.execute(query)
word_list = cur.fetchall()
cur.close()

DB_NAME = "frtoenwords"

__db = MySQLdb.connect(host=DB_HOST ,user=DB_USER ,passwd=DB_PASS,db=DB_NAME, charset = "utf8", use_unicode = True)
__db.autocommit(True)
cur = __db.cursor()

for word in word_list:
    try:
        en_word = translatejson.translate(word[1].encode("utf-8"))
        if en_word != word[1]:
            query = "insert into words values (NULL,'%s', '%s','%s')" % (word[2], word[1], en_word)
            cur.execute(query)
        else:
            print "Same word: %s" % word[1]
    except:
        print "Bad word: %s" % word[1]
        sleep(2)
