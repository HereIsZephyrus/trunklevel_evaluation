# encoding:utf-8
import requests 
#import pandas as pd
import csv
import os
from datetime import datetime

def main():
    current_time = datetime.now()
    start_time = current_time.strftime(r"%d_%H_%M");
    #print("开始请求时间:", start_time)

    url = "https://api.map.baidu.com/traffic/v1/bound"
    ak = os.environ.get('API_KEY')
    evaluation = []
    sectionInfo = []
    params = {
        "bounds":    "30.548317,114.293140;30.549021,114.294639",
        "coord_type_input":    "wgs84",
        "coord_type_output":    "gcj02",
        "ak":       ak,
    }
    response = requests.get(url=url, params=params)
    if response:
        data = response.json()
        if (data["status"] == 0):
            evaluation.append(data["evaluation"])
            trafficinfo = data["road_traffic"]
            if "congestion_sections" in trafficinfo:
                sections = trafficinfo["congestion_sections"]
                for section in sections:
                    sectionItem = {
                        'time' : start_time,
                        "distance" : section["congestion_distance"],
                        "speed" : section["speed"],
                        "status" : section["status"],
                        "trend" : section["congestion_trend"],
                    }
                    sectionInfo.append(sectionItem)
    current_time = datetime.now()
    term_time = current_time.strftime(r"%d_%H_%M");
    #print("结束请求时间:", term_time)
        
    if not os.path.exists('./result/focus_info.csv'):
        os.makedirs(os.path.dirname('./result/focus_info.csv'), exist_ok=True)
    with open('./result/focus_info.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        evaluation.insert(0,f'{start_time}-{term_time}')
        writer.writerow(evaluation)

    if not os.path.exists('./result/focus_trunksection.csv'):
        os.makedirs(os.path.dirname('./result/focus_trunksection.csv'), exist_ok=True)
    with open('./result/focus_trunksection.csv', mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['time','distance', 'speed', 'status','trend']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sectionInfo)

if __name__ == '__main__':
    main()