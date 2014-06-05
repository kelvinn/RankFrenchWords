import MySQLdb
import csv

DB_HOST = "localhost"
DB_USER = "frenchwords"
DB_PASS = "bonjour"
DB_NAME = "frtoenwords"

__db = MySQLdb.connect(host=DB_HOST ,user=DB_USER ,passwd=DB_PASS,db=DB_NAME, charset = "utf8", use_unicode = True)
__db.autocommit(True)
cur = __db.cursor()

wordWriter = csv.writer(open('wordlist.csv', 'w'), delimiter=' ',
                         quotechar='|', quoting=csv.QUOTE_MINIMAL)

query = "select * from words order by wordcount DESC"
cur.execute(query)
word_list = cur.fetchall()
row_list = []
i = 1
for word in word_list:
    row_list.append(word[0])
    row_list.append(word[2].encode("utf-8"))
    row_list.append(word[3].encode("utf-8"))
    if i % 3 == 0:
        wordWriter.writerow(row_list)
        print row_list
        row_list = []
        i = 0
    i = i + 1


