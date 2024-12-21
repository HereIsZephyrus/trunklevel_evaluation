# encoding:utf-8
import requests 
#import pandas as pd
import csv
import os
from datetime import datetime
from datetime import timedelta

def main():
    current_time = datetime.now() + timedelta(hours=8)
    start_time = current_time.strftime(r"%d-%H-%M");
    #print("开始请求时间:", start_time)

    url = "https://api.map.baidu.com/traffic/v1/road"
    ak = os.environ.get('API_KEY')
    roads = ['京汉大道','江汉路']
    if not os.path.exists('./result/focus_basic_info.csv'):
        os.makedirs(os.path.dirname('./result/basic_info.csv'), exist_ok=True)
        with open('./result/basic_info.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            header = roads.copy()
            header.insert(0,'name')
            writer.writerow(header)
    if not os.path.exists('./result/focus_section_info.csv'):
        os.makedirs(os.path.dirname('./result/focus_section_info.csv'), exist_ok=True)
        with open('./result/focus_section_info.csv', mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['name','time','distance', 'speed', 'status','trend']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    basicInfo = []
    sectionInfo = []
    for road in roads:
        params = {
        "road_name":road,
        "city":    "武汉市",
        "ak":       ak,
        }
        response = requests.get(url=url, params=params)
        if response:
            data = response.json()
            if (data["status"] == 0):
                evaluation = data["evaluation"]
                basicInfo.append(evaluation["status"])
                trafficinfo = data["road_traffic"][0]
                if "congestion_sections" in trafficinfo:
                    sections = trafficinfo["congestion_sections"]
                    for section in sections:
                        sectionItem = {
                            'name' : road,
                            'time' : start_time,
                            "distance" : section["congestion_distance"],
                            "speed" : section["speed"],
                            "status" : section["status"],
                            "trend" : section["congestion_trend"],
                        }
                        sectionInfo.append(sectionItem)
    current_time = datetime.now() + timedelta(hours=8)
    term_time = current_time.strftime(r"%d_%H_%M");
    #print("结束请求时间:", term_time)
        
    with open('./result/focus_basic_info.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        basicInfo.insert(0,f'{start_time}')
        writer.writerow(basicInfo)

    with open('./result/focus_section_info.csv', mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['time','distance', 'speed', 'status','trend']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerows(sectionInfo)

if __name__ == '__main__':
    main()