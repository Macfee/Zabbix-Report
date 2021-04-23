# -*- coding: utf-8 -*-
import preppy
from z3c.rml import rml2pdf
import requests

import os
import datetime
import json

class Api:
    def __init__(self):
        self.session = requests.session()
        self.url = 'http://8.8.8.8/api_jsonrpc.php'
        self.username = "Admin"
        self.password = "test123"
        self.headers = {'Content-Type': 'application/json'}
        self.current_date = datetime.datetime.now().strftime("%Y%m%d")
        auth = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.username,
                "password": self.password
            },
            "id": 0,
            "auth": None,
        }
        requests.encoding = "utf8"
        response = self.session.post(self.url, data=json.dumps(auth), headers=self.headers)
        self.authid = json.loads(response.text)['result']
        self.cookie = {'zbx_sessionid':self.authid}


    def fetchDataGraph(self, graph_id):
        data = self.session.get("http://172.16.0.119/chart2.php?graphid={graph_id}&from=now-1d%2Fd&to=now-1d%2Fd&profileIdx=web.graphs.filter&profileIdx2={graph_id}&width=600&height=150&_=ube2loaa&screenid=".format(graph_id=graph_id), stream=True, headers=self.headers, cookies=self.cookie)
        if not os.path.exists("images/%s" % self.current_date): os.makedirs("images/%s" % self.current_date)
        with open("images/%s/%s.png" % (self.current_date, graph_id), "wb") as fd:
            for chunk in data.iter_content():       
                fd.write(chunk)

    def testToGeneratePDF(self):
        template = preppy.getModule('./template.prep')
	current_date = self.current_date
        rmlText = template.get(current_date, pic_data)
        pdf = rml2pdf.parseString(rmlText)
        if not os.path.exists("./output"): os.makedirs("./output")
        f = open("./output/服务器监控指标-%s.pdf" % self.current_date, "w+")
        f.write(pdf.read())
        f.close()


if __name__ ==  "__main__":
    
    pic_data = [
        {"name": "Nginx状态", "data": (1404, 1405)},
        {"name": "Redis状态", "data":  (1404, 1405)},
        {"name": "MYSQL指标", "data":  (1404, 1405)},
        {"name": "CPU 使用率", "data":  (1404, 1405)},
        {"name": "IO Stat", "data":  (1404, 1405)},
        {"name": "磁盘使用率", "data":  (1404, 1405)},
        {"name": "内存可用率", "data":  (1404, 1405)},
        {"name": "网络流量", "data":  (1404, 1405)},
    ]
    api = Api()
    for v in pic_data:
        for x in v['data']:
        # if os.path.exists("images/%s/%s.png" % (current_date, x)):
        #    continue
            api.fetchDataGraph(x)
    api.testToGeneratePDF()
