import requests
import time
import random
import pymysql
import telebot
import re
from bs4 import BeautifulSoup
import datetime

connection= pymysql.connect(
    host='localhost',
    port= 3306,
    user='root',
    passwd='1234512345',
    database='game_stat',
    cursorclass=pymysql.cursors.DictCursor
)
print(connection)

with connection.cursor() as cursor:
    # Read a single record
    # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
    cursor.execute("SELECT  distinct   player, status FROM game_stat.indextable5;")
    result = cursor.fetchall()
    # connection.close()
print('yttytuyt')
i = 0
stlist =[]
stlist2 = []
# for r in result:
#     st1 = r['player'], r['status']
#     for r2 in result:
#         st2 = r2['player'], r2['status']
#         if st1 == st2 and st1 not in stlist: #перепроверить, возможна ошибка если у игрока одна игра
#             i = i+1
#             print(i, st1)
#             stlist.append(st1)
#     print(r['id'])

for r in result:
    st1 = r['player'], r['status']
    stlist.append(st1)

for sl in enumerate(stlist):
   print(sl)

# print(r['id'], r['player'], '              ', r['status'])

for s in stlist:
    st1 = s[0], s[1]
    # print(st1)
    for s2 in stlist:
        st2 = s2[0], s2[1]
        # print(st2)
        if st1[0] == st2[0] and st1[1] != st2[1] :

            stlist2.append(st1)
            print(st1)
stlist2.reverse()
print('==================================')
i = 0
stlist3 =[]
stlist4 =[]
for sl in stlist2:
    if sl[0] not in stlist3:
          stlist3.append(sl[0])
          stlist4.append(sl)
          i = i + 1
          print(i, sl)
print('==================================')
i = 0
for sl in stlist4:
      i = i + 1
      print(i, sl)

with connection.cursor() as cursor:
    for sl in stlist4:
        upd = f'UPDATE game_stat.indextable5 SET status = "{sl[1]}" WHERE player = "{sl[0]}"'
        print(upd)
        cursor.execute(upd)
        connection.commit()
    connection.close()
print('xxxxxxxxxx')