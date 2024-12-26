import pandas as pd

Lsafe = 0.03 # fluent distace : 30m
viewGap = 0.4 # about 20-30 minutes
roadInfo = pd.read_csv('./innerroad_infos.csv')
#focus_roadInfo = pd.read_csv('./focus_innerroad_infos.csv')
congestion = pd.read_csv('./result/section_info_adjust.csv')
#focus_congestion = pd.read_csv('./result/focus_section_info.csv')
roads = pd.read_csv('./result/basic_info_adjust.csv')
#focus_road = pd.read_csv('./result/focus_basic_info.csv')
n = [860,702,576] # 2,3,4
averv = [17,12,6]
dt = 0
ds = 0
for indexr,road in roads.iterrows():
    if indexr == 0:
        continue
    for indexi,info in roadInfo.iterrows():
        if indexi == 0:
            continue
        name = info['name']
        congestionCapacity = int(info['congestion'])
        status = int(roads[name][1])
        vmin = congestionCapacity * Lsafe
        length = float(info['length']) /1000
        dt = dt + length * (1 / averv[status - 2] - 1 / vmin) * viewGap * n[status - 2] * 2 #minites per 10 minites
        ds = ds + dt * vmin

for indexi,info in roadInfo.iterrows():
    if indexi == 0:
        continue
    name = info['name']
    for indexc,section in congestion.iterrows():
        if indexc == 0:
            continue
        if (section['name'] == name):
            congestionCapacity = int(info['congestion'])
            status = int(section['status'])
            vmin = congestionCapacity * Lsafe
            length = float(section['distance']) /1000
            vreal = float(section['speed'])
            subdt = length * (1 / averv[status - 2] - 1 / vmin) * viewGap * n[status - 2] * 2
            dt = dt + length * n[status - 2] * (1 / vreal - 1 / vmin) * 2 - subdt
            ds = ds + dt * vmin - subdt * vmin

print(ds)
print(dt)