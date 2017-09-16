import requests
from lxml import etree

import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText

import json

import os

def getExtIP():
    response = requests.get("http://www.canyouseeme.org/");
    html = etree.HTML(response.text);
    result = html.xpath("//input[@name='IP']/@value");
    if(len(result)!=0):
        return result[0];


def getIntIP():
    # 命令行 hostname -I 只适用于树莓派
    textlist = os.popen("hostname -I").read().split();
    return textlist[0];



def getPort():
    response = requests.get("http://www.canyouseeme.org/");
    html = etree.HTML(response.text);
    result = html.xpath("//input[@name='port']/@value");
    if(len(result)!=0):
        return result[0];



def sendMail():
    # 先登录校园网
    loginSTU();
    body = "Pi's IntIP" + getIntIP() + "Pi's ExtIP:  " + getExtIP() + "\nPi's port: " + getPort();
    ret = True;
    try:
        msg = MIMEText(body, 'plain', 'utf-8');
        msg['From'] = formataddr(["Raspberry of djwang", "djwangstu@163.com"]);
        msg['To'] = formataddr(["SchoolMail of djwang", "15djwang@stu.edu.cn"]);
        msg['Subject'] = "Raspberry Pi login";

        server = smtplib.SMTP("smtp.163.com", 25);
        server.login("djwangstu@163.com", "wswdjCS6513861");
        server.sendmail("djwangstu@163.com", ["15djwang@stu.edu.cn",], msg.as_string());
        server.quit();
    except Exception:
        ret = False;
    return ret;


def loginSTU():
    url = "http://a.stu.edu.cn/ac_portal/login.php";
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Referer': 'http://a.stu.edu.cn/ac_portal/20160808100633/pc.html?template=20160808100633&tabs=pwd&vlanid=0&url=',
        'Host': 'a.stu.edu.cn',
        'Origin': 'http://a.stu.edu.cn',
    }
    postData = {'opr': 'pwdLogin',
                'userName': "15djwang",
                'pwd': "wswdjCS6513861",
                'rememberPwd': '0'};

    response = requests.post(url=url, data=postData, headers=headers);
    response.encoding = 'utf-8';
    jsonstr = response.text.replace('\'', '\"');
    jsondata = json.loads(jsonstr)
    result = [jsondata["success"], jsondata["msg"]];
    return result;



def testMail():
    ret = sendMail();
    if ret:
        print("send success");
    else:
        print("send fail");




if __name__ == '__main__':
    sendMail();







