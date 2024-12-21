## github action 6 a. m. to 12.p.m 10 minites per time
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
    roads = ['江汉北路','黎黄陂路','江汉路','保华街','旅顺路','中北路','上海路','民意上街','公安路','大连路','大兴一路','车站路','七星路','义和巷','大兴二路','黄兴路','和平大道','松竹路','单洞三路','团结路','岳飞街','台北路','瑞祥路','京汉大道','民意一路','郝梦龄路','解放大道','宏昌路','姚家岭街','合作路','秦园中路','前进二路','一马路','洞庭小路','武胜路','三民路','解放公园路','江汉一路','火炬路','汇通路','荆南街','晴川桥','芦沟桥路','武汉长江公铁隧道','三新横街','滨江大道','友谊路','知音大道','沙湖大道','沙湖大桥','天津路','张自忠路','沙湖路','五福路','球场街','体育馆路','利济北路','大兴路','香港路','梅苑路','武珞路六巷','健康路','长喻路','前进路','花楼街','龟山南路','沿江大道','五福小路','江汉四路','红巷','民意三路','民意四路','友益街','新生路','西马路','前进四路','晴川街','武汉长江隧道','青岛路','万松园路','单洞路','黄鹤楼东路','胭脂路','一元路','云架桥','徐东大街','民主一街','烟霞路','公正路','自治街','公平路','楚汉路','后街','京汉街','珞喻路','沙湖环路','统一街','建设街','交易横街','首义路','民权路','解放南路','武车路','学院路','山海关路','多福路','武珞路二巷','中南二路','中华路','球场横街','临江大道','武展东路','民主二街','解放路','武商路','尚隆路','武珞路辅路','洞庭街','拦江路','黄石路','汉正街','江汉二路','四马路','舒家街','团结大道','韶华路','汉中路','六合路','积玉路','高公街','紫沙路','武汉大道','兴国南路','兰陵路','前进五路','民主路','武汉长江大桥','民主街','交通路','武珞路','保成路','前进一路','游艺路','中南一路','铭新街','长江隧道','四唯路','中南三路','粮道街','鹦鹉大道','沿河大道','民族路','麟趾路','二曜路','北京路','中山路','东湖西路','江汉桥','小龟山路','新马路','顺道街','宏茂巷','大东门立交','黄浦大街','三阳路','中山大道','惠安路','秦园东路','南京路','书卷路','胜利街','满春路','新兴街','民生路','崇善路','武展西路','大智路','武珞路五巷','长春街','清芬一路','团结南路','宏祥路','民主二路','沙湖苑路','鄱阳街','蔡锷路','中南路','武昌路','大夹街','新生小路','友谊南路','昙华林','秦园路','千家街','友谊大道','黄陂街','交易街','武汉长江公铁隧道','黄鹤楼隧道']
    if not os.path.exists('./result/basic_info.csv'):
        os.makedirs(os.path.dirname('./result/basic_info.csv'), exist_ok=True)
        with open('./result/basic_info.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            header = roads.copy()
            header.insert(0,'name')
            writer.writerow(header)
    if not os.path.exists('./result/section_info.csv'):
        os.makedirs(os.path.dirname('./result/section_info.csv'), exist_ok=True)
        with open('./result/section_info.csv', mode='w', newline='', encoding='utf-8') as file:
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
        
    with open('./result/basic_info.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        basicInfo.insert(0,f'{start_time}')
        writer.writerow(basicInfo)

    with open('./result/section_info.csv', mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['time','distance', 'speed', 'status','trend']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerows(sectionInfo)

if __name__ == '__main__':
    main()