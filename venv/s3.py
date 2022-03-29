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


headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.63"
    }

def pars_indextable5():
    tablename='indextable5'

    '''
    
    with connection.cursor() as cursor:
            tabl = f"CREATE TABLE {tablename} (id int AUTO_INCREMENT," \
                   f"number varchar(4) ," \
                   f"player varchar(45) ," \
                   f"status varchar(45) ," \
                   f"pos varchar(4)," \
                   f"min varchar(26) ," \
                   f"fgm_a varchar(16) ," \
                   f"3pm_a varchar(16) ," \
                   f"ftm_a varchar(16) ," \
                   f"fic decimal(5,0) ," \
                   f"off int ," \
                   f"def int ," \
                   f"reb int ," \
                   f"ast int ," \
                   f"pf int ," \
                   f"stl int ," \
                   f"blk int ," \
                   f"too int ," \
                   f"pts int," \
                   f"data varchar(26) ,PRIMARY KEY (id));"
            cursor.execute(tabl)
            print('table')
    '''

    x=1 # количество дней назад
    while x>=1: #
        t= datetime.datetime.today() - datetime.timedelta(days=x)
        tdata = t.date()
        data_game=tdata.strftime("%d_%m_%Y")
        url = "https://basketball.realgm.com/nba/scores/{0}/All".format(tdata)
        print(url)
        print(tdata, data_game)
        print(type(data_game))

        req = requests.get(url, headers=headers)
        src = req.text
        #print(src)

        #
        # with open("indexS.html", "w", encoding='utf8') as file:
        #      file.write(src)
        #
        # with open("indexS.html", encoding='utf-8') as file:
        #     src = file.read()
        #

        soup = BeautifulSoup(src, "html.parser")
        t = soup.find(class_="large-column-left scoreboard").find_all('a', text='Box Score')
        i = 0
        a = []
       # print(soup)
        for link in t:
            link = 'https://basketball.realgm.com' + link.get('href')
            a.append(link)
            print(i, a[i])
            i = i + 1

        count = 0
        for w in a:
           # if count < 5:
                print(tdata)
                req = requests.get(url=w, headers=headers)
                src = req.text
                #print(src)

                #
                # with open("indexS2.html", "w", encoding='utf8') as file:
                #  file.write(src)
                #
                # with open("indexS2.html", encoding='utf-8') as file:
                #     src = file.read()

                count = count + 1
                t = random.randrange(6, 23)
                print(t)
                time.sleep(t)
                # print(src)
                soup = BeautifulSoup(src, 'html.parser')
                head = soup.find(class_="boxscore-gamedetails").find_all('a')  # собираем название команд
                k1 = (head[0].text)  # присваиваем название первой комманды
                k2 = (head[1].text)  # присваиваем название второй комманды

                t2 = soup.find(class_="tablesaw compact").find('tbody').find_all('tr')  # ищем данные первой комманды
                print(k1)
                for et in t2:
                    z = et.text
                    z = z.strip()  # удаляем  пробелы вначале и вконце
                    z = z.rsplit('\n')  # преобразовываем стр в лист
                    print(z)

                    vall = z
                    vall[2] = k1
                    #vall[2] = k1 + ' - ' + k2
                    vall.append(data_game)
                    vall = tuple(vall)
                    val = []
                    val.append(vall)
                    print(val)
                    sql = f"INSERT INTO {tablename} (number,player,status,pos,min,fgm_a,3pm_a,ftm_a,fic,off,def,reb,ast,pf,stl,blk,too,pts,data ) " \
                          f"VALUES ( %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s)"

                    cursor = connection.cursor()
                    print(type(z))
                    cursor.executemany(sql, val)
                    connection.commit()
                    #connection.close()

                #vall = [ '7','Obi Toppin', 'Bench', 'PF', '15-08', '3-9', '0-0', '1-2', '7', '4', '4', '8', '1', '1', '0', '1', '1', '7']
                print(k2)
                t3 = soup.find(class_="tablesaw compact").find_next(class_="tablesaw compact").find('tbody').find_all(
                    'tr')  # ищем данные второй комманды
                print(k2)
                for et in t3:
                    z = et.text
                    z = z.strip()  # удаляем  пробелы вначале и вконце
                    z = z.rsplit('\n')  # преобразовываем стр в лист
                    print(z)

                    vall = z
                    vall[2] = k2
                    #vall[2] = k2 +' - '+ k1
                    vall.append(data_game)
                    vall = tuple(vall)
                    val = []
                    val.append(vall)
                    print(val)
                    sql = f"INSERT INTO {tablename} (number,player,status,pos,min,fgm_a,3pm_a,ftm_a,fic,off,def,reb,ast,pf,stl,blk,too,pts,data ) " \
                          f"VALUES ( %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s)"
                    #print(type(z))
                    cursor = connection.cursor()
                    cursor.executemany(sql, val)
                    connection.commit()

        x = x - 1
    # connection.close()



def pars_tablegameday():

    tablename2='tablegameday'
    tablename3='bdgameday'

    # with connection.cursor() as cursor:
    #         tabl = f"CREATE TABLE {tablename2} (id int AUTO_INCREMENT," \
    #                f"p3time varchar(15) ," \
    #                f"p3teamviz varchar(45) ," \
    #                f"p3teamhome varchar(45) ," \
    #                f"tvizwl varchar(45) ," \
    #                f"thomwl varchar(45) ," \
    #                f"p3status varchar(45) ," \
    #                f"p3listvizit varchar(250) ," \
    #                f"p3listvizit100 varchar(250) ," \
    #                f"p3listvizit75 varchar(250) ," \
    #                f"p3listvizit50 varchar(250) ," \
    #                f"p3listvizit25 varchar(250) ," \
    #                f"p3listvizit0 varchar(250) ," \
    #                f"p3status2 varchar(45) ," \
    #                f"p3listhome varchar(250) ," \
    #                f"p3listhome100 varchar(250) ," \
    #                f"p3listhome75 varchar(250) ," \
    #                f"p3listhome50 varchar(250) ," \
    #                f"p3listhome25 varchar(250) ," \
    #                f"p3listhome0 varchar(250) ," \
    #                f"p3date varchar(12) ,PRIMARY KEY (id));"
    #         cursor.execute(tabl)
    #         print('table')


    url2 = "https://www.rotowire.com/basketball/nba-lineups.php"
    print(url2)
    req2 = requests.get(url2, headers=headers)
    src2 = req2.text
    # print(src2)
    #
    # with open("indexScan222.html", "w", encoding='utf8') as file:
    #      file.write(src2)

    # with open("indexScan222.html", encoding='utf-8') as file:
    #      src2 = file.read()

    soup = BeautifulSoup(src2, "html.parser")
    #print(src2)
    val2 = []
    val4=[]
    p3date = 'q'
    pagedata = soup.find(string=re.compile("Starting lineups for"))
    # for p in pagedata.strings:
    #      print(p(0))
    #pagedata = ss.find(class_="page-title__secondary")
    parsinfo2 = soup.find_all(class_="lineup is-nba")
    for ss in parsinfo2:

        p3time = ss.find(class_="lineup__time").get_text(strip=True)
        #p3timel = p3time.text
        #p3timel = p3timel.strip()  # удаляем  пробелы вначале и вконце
        #p3timel = p3timel.rsplit('\n')
        val2.append(p3time)
        print(p3time)
        p3teamviz = ss.find(class_="lineup__team is-visit").get_text(strip=True)
        val2.append(p3teamviz)
        print(p3teamviz)
        p3teamhome = ss.find(class_="lineup__team is-home").get_text(strip=True)
        val2.append(p3teamhome)
        print(p3teamhome)
        tvizwl = ss.find(class_="lineup__wl").get_text(strip=True)
        val2.append(tvizwl)
        print(tvizwl)#
        thomwl = ss.find(class_="lineup__wl").find_next(class_="lineup__wl").get_text(strip=True)
        val2.append(thomwl)
        print(thomwl)

        p3status = ss.find(class_="lineup__list is-visit").find('li').get_text(strip=True)
        val2.append(p3status)
        print(p3status)

        p3listvizit = ss.find(class_="lineup__list is-visit").find_all( class_="lineup__player is-pct-play-100" )
        t=''
        for p33 in p3listvizit:
            p33l = p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3listvizit100 = ss.find(class_="lineup__list is-visit").find_all(class_="lineup__player is-pct-play-100 has-injury-status")
        t=''
        for p33 in p3listvizit100:
            p33l = p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3listvizit75 = ss.find(class_="lineup__list is-visit").find_all(class_="lineup__player is-pct-play-75 has-injury-status")
        t=''
        for p33 in p3listvizit75:
            p33l = p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3listvizit50 = ss.find(class_="lineup__list is-visit").find_all(class_="lineup__player is-pct-play-50 has-injury-status")
        t=''
        for p33 in p3listvizit50:
            p33l = p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3listvizit25 = ss.find(class_="lineup__list is-visit").find_all(class_="lineup__player is-pct-play-25 has-injury-status")
        t=''
        for p33 in p3listvizit25:
            p33l = p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3listvizit0 = ss.find(class_="lineup__list is-visit").find_all(class_="lineup__player is-pct-play-0 has-injury-status")
        t=''
        for p33 in p3listvizit0:
            p33l=p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3status2 = ss.find(class_="lineup__list is-home").find('li').get_text(strip=True)
        val2.append(p3status2)# тут было опечатка
        print(p3status2)

        p3listhome = ss.find(class_="lineup__list is-home").find_all(class_="lineup__player is-pct-play-100")
        t=''
        for p33 in p3listhome:
            p33l = p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3listhome100 = ss.find(class_="lineup__list is-home").find_all(class_="lineup__player is-pct-play-100 has-injury-status")
        t=''
        for p33 in p3listhome100:
            p33l = p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3listhome75 = ss.find(class_="lineup__list is-home").find_all(class_="lineup__player is-pct-play-75 has-injury-status")
        t=''
        for p33 in p3listhome75:
            p33l = p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3listhome50 = ss.find(class_="lineup__list is-home").find_all(class_="lineup__player is-pct-play-50 has-injury-status")
        t=''
        for p33 in p3listhome50:
            p33l = p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3listhome25 = ss.find(class_="lineup__list is-home").find_all(class_="lineup__player is-pct-play-25 has-injury-status")
        t=''
        for p33 in p3listhome25:
            p33l = p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3listhome0 = ss.find(class_="lineup__list is-home").find_all(class_="lineup__player is-pct-play-0 has-injury-status")
        t=''
        for p33 in p3listhome0:
            p33l = p33.find('a')
            t = t + p33l.get('title') + ', '
            print(p33l.get('title'))
        val2.append(t)

        p3date = datetime.datetime.now()
        p3date = p3date.date().strftime("%d.%m.%Y")
        val2.append(p3date)

        val4.append(list(val2))
        val2 = []


            #print(type(p33l))
    print(val2)
    # tablegameday
    valzapis2=[]
    valzapis=[]
    # print(p3date)
    timeobj = datetime.time(23, 59, 59)
    timeobj_end = datetime.time(12, 0, 0)
    with connection.cursor() as cursor:
        # zapros = "SELECT p3date FROM game_stat.bdgameday"
        cursor.execute("SELECT p3date FROM game_stat.bdgameday WHERE id=(SELECT max(id) FROM game_stat.bdgameday)")
        p3datestr = cursor.fetchone()
        print('p3datestr=', p3datestr)
        datekonv = datetime.datetime.strptime(p3datestr.setdefault('p3date'), '%d.%m.%Y').date()#переводим p3datestr в date
        p3date2 = datetime.datetime.now().date()# текущая дата
        p3time = datetime.datetime.now().time()  # текущаее время
        # if p3time > timeobj and p3time < timeobj_end:
        #     print('p3time=', p3time)
        datekonv = datekonv - datetime.timedelta(days=1)
        print('datekonv=', datekonv)
        datezap = datetime.datetime.now().date() - datetime.timedelta(days=1)
        # print(type(datezap), datezap)
        datezap = datezap.strftime("%d.%m.%Y")
        # print(type(datezap), datezap)
        s = p3date2 - datekonv
        print( 's=', s)
        print( "datezap" , datezap) # дата последней записи
    print('p3date=' , p3date)

    if s >= datetime.timedelta(days=2) and p3time < timeobj and p3time > timeobj_end:
        # valp = val4[0].pop()
        # for v in val4:
        #     v[-1] = datezap # изменяем дату минус 1
        print(val4)
        print(s , 'Делаем запись bdgame')
        sql = f"INSERT INTO {tablename3} (p3time ,p3teamviz ,p3teamhome ,tvizwl ,thomwl ,p3status ,p3listvizit ,p3listvizit100 ,p3listvizit75 ,p3listvizit50 ,p3listvizit25 ,p3listvizit0 ,p3status2 ,p3listhome ,p3listhome100 ,p3listhome75 ,p3listhome50 ,p3listhome25 ,p3listhome0 ,p3date) " \
              f"VALUES ( %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s)"
        cursor = connection.cursor()
        cursor.executemany(sql, val4)
        connection.commit()
        for v in val4:
            v[-1] = p3date# изменяем дату плюс 1
    if p3date != 'q':
        sql = f"INSERT INTO {tablename2} (p3time ,p3teamviz ,p3teamhome ,tvizwl ,thomwl ,p3status ,p3listvizit ,p3listvizit100 ,p3listvizit75 ,p3listvizit50 ,p3listvizit25 ,p3listvizit0 ,p3status2 ,p3listhome ,p3listhome100 ,p3listhome75 ,p3listhome50 ,p3listhome25 ,p3listhome0 ,p3date) " \
                              f"VALUES ( %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s)"
        cursor = connection.cursor()
        #cursor.executemany("DELETE FROM %s", (tablename2,))
        cursor.execute(f'DELETE FROM  {tablename2}')
        # cursor.execute('DELETE FROM tablegameday')
        # connection.commit()
        cursor.executemany(sql, val4)
        print( 'Делаем запись tablegame')
    connection.commit()
    print('val4=', val4)
    connection.close()

    p3date2 = datetime.datetime.now().strftime("%d.%m.%Y  %H:%M ")
    # print(p3date2)
    # print(str(pagedata))


if __name__ == "__main__":
    pars_indextable5()

    t = random.randrange(6, 23)
    print(t)
    time.sleep(t)

    pars_tablegameday()


#class="lineup__player is-pct-play-100 has-injury-status"
    #print(ss.text.rstrip())
# parsinfo2 = soup.find_all(class_="lineup__team is-visit")



# par3 = parsinfo2.find_all(class_="lineup__time")
# vr = parsinfo2
# #vr.get_text()
# print(par3)

# print(val2)
# tablename2='tablegameday'
# valzapis2=[]
# valzapis = ['fsfsf','2' ,'3' ,'4' ,'5','1','2' ,'3' ,'4' ,'5','1','2' ,'3' ,'4' ,'5','1','2' ,'3' ,'3']
# for v in valzapis:
#      v = v.rsplit('\n')
#      valzapis2.append(v)
# valzapis2=tuple(valzapis2)
# a=[]
# a.append(valzapis2)
# print(valzapis)
# print(valzapis2)
# print(type(valzapis))
# print(type(valzapis2))
# print(type(a))
# sql = f"INSERT INTO {tablename2} (p3time ,p3teamviz ,p3teamhome ,tvizwl ,thomwl ,p3status ,p3listvizit ,p3listvizit100 ,p3listvizit75 ,p3listvizit50 ,p3listvizit25 ,p3listvizit0 ,p3status2 ,p3listhome ,p3listhome100 ,p3listhome75 ,p3listhome50 ,p3listhome25 ,p3listhome0) " \
#                       f"VALUES ( %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s)"
# cursor = connection.cursor()
# cursor.executemany(sql, a)
# connection.commit()