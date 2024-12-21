import pandas as pd

Lsafe = 0.06 # safe distace : 60m
viewGap = 10
roadInfo = pd.read_csv('./innerroad_infos.csv')
#congestion = pd.read_csv('./section_info.csv')
focus_congestion = pd.read_csv('./result/focus_section_info.csv')
#roads = pd.read_csv('./basic_info.csv')
focus_road = pd.read_csv('./result/focus_basic_info.csv')
n = [1000,2000,3000] # 2,3,4
dt = 0
ds = 0
for indexi,info in roadInfo.iterrows():
    if indexi == 0:
        continue
    name = info['name']
    for indexr,road in focus_road.iterrows():
        if indexr == 0:
            continue
        
for indexi,info in roadInfo.iterrows():
    if indexi == 0:
        continue
    name = info['name']
    for indexc,section in focus_congestion.iterrows():
        if indexc == 0:
            continue
        if (section['name'] == name):
            congestionCapacity = int(info['congestion'])
            status = int(section['status'])
            vmin = congestionCapacity * Lsafe
            length = float(section['distance']) /1000
            vreal = float(section['speed'])
            dt = dt + length * n[status - 2] * (1 / vreal - 1 / vmin)  #* viewGap minites per 10 minites
            ds = ds + dt * vmin

print(ds)
print(dt)