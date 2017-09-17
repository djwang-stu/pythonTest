# -*- coding: utf-8 -*-
import requests
from lxml import etree

import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText

import json

import os
import socket
import platform

def getExtIP():
    # we provide two kinds of method to query external ip. Network is needed
    # one by getting ip from ifconfig.me api
    # the other by getting ip from website spider
    ip = False;
    try:
        ip = os.popen("curl ifconfig.me/ip").read();
        if(len(ip) == 0):
            raise Exception("\033[1;32;40mget ip from ifconfig.me failed\033[0m")
    except Exception as e:
        print(e);
        try:
            response = requests.get("http://www.canyouseeme.org/");
            html = etree.HTML(response.text);
            result = html.xpath("//input[@name='IP']/@value");
            if(len(result)!=0):
                ip = result[0];
        except Exception:
            print("\033[1;32;40mget ip from website-spider failed\033[0m")
    return ip;



def getIntIP():
    #if the network lost its connection, ip will be simply 127.0.0.1
    ip = socket.gethostbyname(socket.gethostname())
    sysstr = platform.system();
    if((ip=="127.0.0.1") & (sysstr=="Linux")):
        # command 'hostname -I' is available on Linux not macOS
        textlist = os.popen("hostname -I").read().split()
        ip = textlist[0];
    return ip;



def loginSTU(username, password):
    ret = True;
    url = "http://a.stu.edu.cn/ac_portal/login.php";
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Referer': 'http://a.stu.edu.cn/ac_portal/20160808100633/pc.html?template=20160808100633&tabs=pwd&vlanid=0&url=',
        'Host': 'a.stu.edu.cn',
        'Origin': 'http://a.stu.edu.cn',
    }
    postData = {'opr': 'pwdLogin',
                'userName': username,
                'pwd': password,
                'rememberPwd': '0'};
    try:
        response = requests.post(url=url, data=postData, headers=headers);
        response.encoding = 'utf-8';
        jsonstr = response.text.replace('\'', '\"');
        jsondata = json.loads(jsonstr);
        retmsg = [jsondata["success"], jsondata["msg"]];
    except Exception:
        print("\033[1;32;40mlogin in STU failed, check your network or username&password\033[0m")
        ret = False;
    return ret;



def sendMail():
    body = "Pi's IntIP: " + getIntIP() + "\nPi's ExtIP: " + getExtIP()
    ret = True;
    try:
        sender = "djwangstu@163.com";
        password = "wswdjCS6513861"

        msg = MIMEText(body, 'plain', 'utf-8');
        msg['From'] = formataddr(["Raspberry of djwang", "djwangstu@163.com"]);
        msg['To'] =   formataddr(["SchoolMail of djwang","15djwang@stu.edu.cn"]);
        msg['Subject'] = "Raspberry Pi login";

        server = smtplib.SMTP("smtp.163.com", 25);
        server.login("djwangstu@163.com", "wswdjCS6513861");
        server.sendmail("djwangstu@163.com", ["15djwang@stu.edu.cn", ], msg.as_string());
        server.quit();
    except Exception as e:
        # if you send email frequently, the company which provide service may set limitation or prevent you from sending rubbish mail.
        print(e)
        print("\033[1;32;40msending email failed, check your network\033[0m")
        ret = False;
    return ret;

def testMail():
    ret = sendMail();
    if ret:
        print("send success");
    else:
        print("send fail");




if __name__ == '__main__':
    if(loginSTU("15djwang", "wswdjCS6513861")==False):
        loginSTU("15djwang", "wswdjCS6513861")
        sendMail();





