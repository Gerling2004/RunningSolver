import math
import json
import subprocess
import time
import os
from prettytable import PrettyTable

# MuMuManager.exe的绝对路径
mumu_manager_path = r"E:/MuMu/MuMu Player 12/shell/MuMuManager.exe"

#颜色
red =   '\x1b[01;38;5;160m'
blue =  '\x1b[01;38;5;33m'
green = '\x1b[01;38;5;41m'
pink =  '\x1b[01;38;5;211m'
reset = '\x1b[0m'

def calculate_distance(lat1, lon1, lat2, lon2):
    return math.dist((float(lat1), float(lon1)), (float(lat2), float(lon2))) * 111320

def get_route():
    with open("gps.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("route", [])

def update_location(lat, lon, v):
    subprocess.run([mumu_manager_path, "control", "-v", str(v), "tool", "location", "-lon", str(lon), "-lat", str(lat)], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_route(v):
    routes = get_route()

    total_distance = 0
    n = 1

    for i, (lat, lon) in enumerate(routes):
        if i == 0:
            distance = 0
        else:
            distance = calculate_distance(routes[i-1][0], routes[i-1][1], lat, lon)

        total_distance += distance
        update_location(lat, lon, v)

        # 打印状态
        formatted_total_distance = f'{green}{total_distance:.2f}{reset}'
        formatted_distance = f'{green}{distance:.2f}{reset}'
        formatted_n = f'{green}{n}{reset}'
        len_routes = f'{green}{len(routes)}{reset}'

        table = PrettyTable(['      总距离        ', '      步幅        ', '      进度        '])
        table.add_row([f'{formatted_total_distance} M', f'{formatted_distance} M', f'{formatted_n} / {len_routes}'])
        os.system("cls")
        print(f'Mumu {v}')
        print(table)

        time.sleep(1)
        n += 1

    time.sleep(1)

if __name__ == "__main__":
    print(f'''{red}

██████╗ ██╗   ██╗███╗   ██╗███╗   ██╗██╗███╗   ██╗ ██████╗ ███████╗ ██████╗ ██╗    ██╗   ██╗███████╗██████╗ 
██╔══██╗██║   ██║████╗  ██║████╗  ██║██║████╗  ██║██╔════╝ ██╔════╝██╔═══██╗██║    ██║   ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██╔██╗ ██║██╔██╗ ██║██║██╔██╗ ██║██║  ███╗███████╗██║   ██║██║    ██║   ██║█████╗  ██████╔╝
██╔══██╗██║   ██║██║╚██╗██║██║╚██╗██║██║██║╚██╗██║██║   ██║╚════██║██║   ██║██║    ╚██╗ ██╔╝██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝██║ ╚████║██║ ╚████║██║██║ ╚████║╚██████╔╝███████║╚██████╔╝███████╗╚████╔╝ ███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝ ╚═══╝  ╚══════╝╚═╝  ╚═╝
                                                                                                            
                                                                                        Posted by G3rling
          {reset}''')
    v = input(f'请输入模拟器编号:')
    while True:
        process_route(v)
