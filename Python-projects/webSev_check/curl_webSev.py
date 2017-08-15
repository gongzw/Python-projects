#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2017/8/15

def curl_webSev(URL):
    c = pycurl.Curl()
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(c.URL,URL)
    c.setopt(c.CONNECTTIMEOUT, 5)
    c.setopt(c.TIMEOUT, 8)
    c.setopt(c.COOKIEFILE, '')
    c.setopt(c.FAILONERROR, True)
    c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])

    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + "/content.txt",'w') as outfile:
            c.setopt(pycurl.WRITEHEADER,outfile)
            c.setopt(pycurl.WRITEDATA,outfile)
            c.perform()
    except Exception as err:
        print "exec error!\n\t%s" %err
    #    sys.exit()

    print "Http Code:\t%s" %c.getinfo(c.HTTP_CODE)
    print "DNS lookup time:\t%s ms" %(c.getinfo(c.NAMELOOKUP_TIME) * 1000)
    print "Create conn time:\t%s ms" %(c.getinfo(c.CONNECT_TIME) * 1000)
    print "Ready conn time:\t%s ms" %(c.getinfo(c.PRETRANSFER_TIME) * 1000)
    print "Tran Star time:\t%s ms" %(c.getinfo(c.STARTTRANSFER_TIME) * 1000)
    print "Tran Over time:\t%s ms" %(c.getinfo(c.TOTAL_TIME) * 1000)
    print "Download size:\t%d bytes/s" %c.getinfo(c.SIZE_DOWNLOAD)
    print "HTTP header size:\t%d byte" %c.getinfo(c.HEADER_SIZE)
    print "Avg download speed:\t%s bytes/s" %c.getinfo(c.SPEED_DOWNLOAD)
    return c.getinfo(c.HTTP_CODE)

if __name__ == '__main__':
    import os
    import sys
    import time
    import pycurl
    import json
    import MySQLdb
    import subprocess
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    while True:
        with open("server.json","r") as f:
            data = json.load(f)
            for i in data:
                protocol = i
                p_data = data[i]
                for j in p_data:
                    #print "%s service is %s "%(j,p_data[j])

                    service = j
                    s_data = p_data[j]
                    for z in s_data:
                        IP = z
                        PORT = s_data[z]
                        URL = protocol+"://"+IP+":"+PORT+"/"+service+"/"
                        URL = str(URL)
                        print "----test the %s-------"%URL
                        h_code = curl_webSev(URL)
                        if h_code == 200:
                            print "yes"
                        else:
                            content_sql = "set names 'gbk';" + "\n" + "insert into ultrax.msgsend (service, srcNo,destNo,  msgcontent) values ('30','10000', '1891043871', '【万步网】server " + URL +" may be down,pelase check.');"

                            content_sql = content_sql.decode("utf-8")

                            content_sql = content_sql.encode("gbk")



                            try:

                                conn = MySQLdb.Connect(host='192.168.1.8',user='wanbusms',passwd='wanbu@sms',port=3306)

                                cur = conn.cursor()

                                cur.execute(content_sql)

                                cur.close()

                                conn.close()

                            except MySQLdb.Error,e:

                                print "Mysql Error %d: %s" %(e.args[0], e.args[1])



                            time.sleep(300)
